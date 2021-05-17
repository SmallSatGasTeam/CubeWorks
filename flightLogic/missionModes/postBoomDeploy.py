import sys
import subprocess
import time
import os
sys.path.append('../../')
import asyncio
from flightLogic.missionModes import safe
from flightLogic.getDriverData import *
import Drivers.eps.EPS as EPS
from TXISR import prepareFiles
from TXISR import pythonInterrupt
from protectionProticol.fileProtection import FileReset


fileChecker = FileReset()

TRANSFER_WINDOW_BUFFER_TIME = 10 #30 seconds
REBOOT_WAIT_TIME = 900 #15 minutes, 900 seconds

class postBoomMode:

	def __init__(self, saveObject, safeModeObject):
		self.__getTTNCData = TTNCData(saveObject)
		self.__getAttitudeData =  AttitudeData(saveObject)
		self.__tasks = [] # List will be populated with all background tasks
		self.__safeMode = safeModeObject
		self.__timeToNextWindow = -1
		self.___nextWindowTime = -1
		self.__duration = -1
		self.__datatype = -1
		self.__pictureNumber = -1
		self.__startFromBeginning = -1
		fileChecker.checkFile("/home/pi/TXISRData/transmissionFlag.txt")
		self.__transmissionFlagFile = open('/home/pi/TXISRData/transmissionFlag.txt')
		self.__txWindowsPath = ('/home/pi/TXISRData/txWindows.txt')
		fileChecker.checkFile(self.__txWindowsPath)

	async def run(self):
		#Set up background processes
		self.__tasks.append(asyncio.create_task(pythonInterrupt.interrupt()))
		self.__tasks.append(asyncio.create_task(self.__getTTNCData.collectTTNCData(4))) #Post-boom is mode 4
		self.__tasks.append(asyncio.create_task(self.__getAttitudeData.collectAttitudeData()))
		self.__tasks.append(asyncio.create_task(self.__safeMode.thresholdCheck()))
		self.__tasks.append(asyncio.create_task(self.readNextTransferWindow(self.__txWindowsPath)))
		self.__tasks.append(asyncio.create_task(self.rebootLoop()))

		while True:
			while True:
				#if close enough, prep files
				#wait until 5 seconds before, return True
				if(self.__timeToNextWindow is not -1 and self.__timeToNextWindow<14): #If next window is in 2 minutes or less
					if(self.__datatype < 3): #Attitude, TTNC, or Deployment data
						prepareFiles.prepareData(self.__duration, self.__datatype, self.__startFromBeginning, -1)
						print("Preparing data")
					else:
						prepareFiles.preparePicture(self.__duration, self.__datatype, self.__pictureNumber, self.__startFromBeginning)
						print("Preparing Picture data")
					break
				await asyncio.sleep(5)
			windowTime = self.__nextWindowTime
			while True:
				if((windowTime-time.time()) <= 5):
					fileChecker.checkFile('/home/pi/TXISRData/transmissionFlag.txt')
					self.__transmissionFlagFile.seek(0)
					if(self.__transmissionFlagFile.readline()=='Enabled'):
						txisrCodePath = '../TXISR/TXServiceCode/TXService.run'
						print(self.__datatype)
						subprocess.Popen([txisrCodePath, str(self.__datatype)])
						#os.system(txisrCodePath + ' ' + str(self.__datatype) + ' &') #Call TXISR Code
						self.__timeToNextWindow = -1
						break
					else:
						print('Transmission flag is not enabled')
				await asyncio.sleep(0.1) #Check at 10Hz until the window time gap is less than 5 seconds				


	async def rebootLoop(self):
		upTime = 0
		while True:
			if upTime>86400: #Live for more than 24 hours
				if (self.__timeToNextWindow == -1) or (self.__timeToNextWindow > REBOOT_WAIT_TIME):
					self.__safeMode.run(1) #restart, powering off Pi for 1 minute
					print('Rebooting raspberry pi')
					upTime=0
			else:
				print('Uptime: '+str(upTime))
				await asyncio.sleep(60)
				upTime += 60

	async def readNextTransferWindow(self, transferWindowFilename):
		while True:
			#read the given transfer window file and extract the data for the soonest transfer window
			fileChecker.checkFile(transferWindowFilename)
			transferWindowFile = open(transferWindowFilename)
			sendData = 0
			soonestWindowTime = 0
			for line in transferWindowFile:
				#print("reading line: ")
				#print(line)
				data = line.split(",")
				#data[0] = time of next window, data[1] = duration of window, data[2] = datatype, data[3] = picture number
				if(float(data[0]) - time.time() > TRANSFER_WINDOW_BUFFER_TIME):  #if the transfer window is at BUFFER_TIME milliseconds in the future
					if(soonestWindowTime == 0 or float(data[0]) - time.time() < soonestWindowTime):
						soonestWindowTime = float(data[0]) - time.time()
						sendData = data
			if not(sendData == 0):
				#print("Found next transfer window: ")
				#print(sendData)
				self.__timeToNextWindow = float(sendData[0]) - time.time()
				self.__duration = int(sendData[1])
				self.__datatype = int(sendData[2])
				self.__pictureNumber = int(sendData[3])
				self.__nextWindowTime = float(sendData[0])
				self.__startFromBeginning = int(sendData[4])
				#print(self.__startFromBeginning)
				#print(self.__timeToNextWindow)
				#print(self.__duration)
				#print(self.__datatype)
				#print(self.__pictureNumber)
			await asyncio.sleep(3) #Checks transmission windows every 10 seconds

	def cancellAllTasks(self, taskList): #Isn't used in this class, but here anyways
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")
