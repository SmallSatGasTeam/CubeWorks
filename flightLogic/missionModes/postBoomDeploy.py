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
from TXISR import packetProcessing
from protectionProticol.fileProtection import FileReset


fileChecker = FileReset()

TRANSFER_WINDOW_BUFFER_TIME = 10 #30 seconds
REBOOT_WAIT_TIME = 900 #15 minutes, 900 seconds
filePaths = ["~/home/pi/CubeWorks0/TXSIR/TXServiceCode/TXService.run", "~/home/pi/CubeWorks1/TXSIR/TXServiceCode/TXService.run", "~/home/pi/CubeWorks2/TXSIR/TXServiceCode/TXService.run", "~/home/pi/CubeWorks3/TXSIR/TXServiceCode/TXService.run", "~/home/pi/CubeWorks4/TXSIR/TXServiceCode/TXService.run"]
class postBoomMode:

	def __init__(self, saveObject, safeModeObject, codeBase):
		self.__codeBase = codeBase
		self.__getTTNCData = TTNCData(saveObject)
		self.__getAttitudeData =  AttitudeData(saveObject)
		self.__tasks = [] # List will be populated with all background tasks
		self.__safeMode = safeModeObject
		self.__timeToNextWindow = -1
		self.___nextWindowTime = -1
		self.__duration = -1
		self.__datatype = -1
		self.__pictureNumber = -1
		self.__index = -1
		fileChecker.checkFile("/home/pi/TXISRData/transmissionFlag.txt")
		self.__transmissionFlagFile = open('/home/pi/TXISRData/transmissionFlag.txt')
		self.__txWindowsPath = ('/home/pi/TXISRData/txWindows.txt')
		fileChecker.checkFile(self.__txWindowsPath)
		print("Initialized postBoomDeploy")

	async def run(self):
		#Set up background processes
		print("Inside of run in postBoomDeploy")
		self.__tasks.append(asyncio.create_task(pythonInterrupt.interrupt()))
		self.__tasks.append(asyncio.create_task(self.__getTTNCData.collectTTNCData(4))) #Post-boom is mode 4
		self.__tasks.append(asyncio.create_task(self.__getAttitudeData.collectAttitudeData()))
		self.__tasks.append(asyncio.create_task(self.__safeMode.thresholdCheck()))
		self.__tasks.append(asyncio.create_task(self.readNextTransferWindow(self.__txWindowsPath)))
		self.__tasks.append(asyncio.create_task(self.rebootLoop()))
		print("Initalized all tasks.")

		while True:
			print("Inside of first while loop")
			while True:
				print("Inside of second while loop")
				print("WE ARE ABOUT TO PRINT THE DATA TYPE!!!!!!!")
				print(self.__datatype)
				print(self.__timeToNextWindow)
				#if close enough, prep files
				#wait until 5 seconds before, return True
				if(self.__timeToNextWindow is not -1 and self.__timeToNextWindow<14): #If next window is in 14 seconds or less
					if(self.__datatype < 3): #Attitude, TTNC, or Deployment data
						prepareFiles.prepareData(self.__duration, self.__datatype, self.__index)
						print("Preparing data")
					else:
						prepareFiles.preparePicture(self.__duration, self.__datatype, self.__pictureNumber)
						print("Preparing Picture data")
					break
				await asyncio.sleep(5)
			windowTime = self.__nextWindowTime
			while True:
				if((windowTime-time.time()) <= 5):
					fileChecker.checkFile('/home/pi/TXISRData/transmissionFlag.txt')
					self.__transmissionFlagFile.seek(0)
					if(self.__transmissionFlagFile.readline()=='Enabled'):
						txisrCodePath1 = filePaths[self.__codeBase]
						#txisrCodePath = '../TXISR/TXServiceCode/'
						#print(self.__datatype)
						#print(txisrCodePath)
<<<<<<< HEAD
						txisrCodePath = os.path.join(os.path.dirname(__file__), txisrCodePath1)
						print(self.__datatype)
						subprocess.Popen([txisrCodePath, str(self.__datatype)])
						#print("WE ARE ABOUT TO CALL THE C CODE. jajajajajajajajajajajajajajajajajajajajA<><?><?<>><?<?<>?><?<?<?<>?><?<>?<?><?<?<>?<?<?><?><?<>?")
						#subprocess.Popen(['cd', ';', 'cd', str(txisrCodePath), ';', 'sudo', './TXService.run', str(self.__datatype)])
						#os.system("cd " + str(txisrCodePath) + " ; sudo ./TXService.run " + str(self.__datatype)) #Call TXISR Code
=======
						print("WE ARE ABOUT TO CALL THE C CODE. jajajajajajajajajajajajajajajajajajajajA<><?><?<>><?<?<>?><?<?<?<>?><?<>?<?><?<?<>?<?<?><?><?<>?")
						#subprocess.Popen(['cd', ';', 'cd', str(txisrCodePath), ';', 'sudo', './TXService.run', str(self.__datatype)])
						os.system("cd ; cd " + str(txisrCodePath) + " ; sudo ./TXService.run " + str(self.__datatype)) #Call TXISR Code
>>>>>>> 3b4635ef5c3434c8740eed25269dd34a51caa17e
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
			print("Inside transfer window.")
			#read the given transfer window file and extract the data for the soonest transfer window
			fileChecker.checkFile(transferWindowFilename)
			transferWindowFile = open(transferWindowFilename)
			sendData = []
			soonestWindowTime = 0

			line = transferWindowFile.readline()
			# print("reading line: ")
			# print(line)
			data = line.split(",")
			# print(data)
			#data[0] = time of next window, data[1] = duration of window, data[2] = datatype, data[3] = picture number
			print(float(data[0]), float(data[0]) - time.time(), TRANSFER_WINDOW_BUFFER_TIME, float(data[0]) - time.time() > TRANSFER_WINDOW_BUFFER_TIME)
			if(float(data[0]) - time.time() > TRANSFER_WINDOW_BUFFER_TIME):  #if the transfer window is at BUFFER_TIME milliseconds in the future
				if(soonestWindowTime == 0 or float(data[0]) - time.time() < soonestWindowTime):
					soonestWindowTime = float(data[0]) - time.time()
					sendData = data
					print("Data: " + str(data))

			if sendData.__len__() == 5:
				print(sendData)
				self.__timeToNextWindow = float(sendData[0]) - time.time()
				self.__duration = int(sendData[1])
				self.__datatype = int(sendData[2])
				self.__pictureNumber = int(sendData[3])
				self.__nextWindowTime = float(sendData[0])
				self.__index = int(sendData[4])
				# print(self.__timeToNextWindow)
				# print(self.__duration)
				# print(self.__datatype)
				# print(self.__pictureNumber)
				# print(self.__index)
			else:
				print("sendData is empty.")
			
			await asyncio.sleep(3) #Checks transmission windows every 10 seconds

	def cancellAllTasks(self, taskList): #Isn't used in this class, but here anyways
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")
