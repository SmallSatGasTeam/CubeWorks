import sys
import subprocess
sys.path.append('../../')
import time
from Drivers.backupAntennaDeployer import BackupAntennaDeployer
from Drivers.antennaDoor import AntennaDoor
import Drivers.eps.EPS as EPS
import asyncio
from flightLogic.missionModes import safe
import flightLogic.getDriverData as getDriverData
from TXISR import pythonInterrupt
from TXISR import packetProcessing
from TXISR import prepareFiles
from protectionProticol.fileProtection import FileReset

fileChecker = FileReset()
TRANSFER_WINDOW_BUFFER_TIME = 10 #30 seconds

class antennaMode:

	def __init__(self, saveObject, safeModeObject):
		self.deployVoltage = 3 #Threshold voltage to deploy
		self.maximumWaitTime = 30 #Maximum time to wait for deployment before going to SAFE
		self.timeWaited = 0 #Time already waited - zero
		self.__getTTNCData = getDriverData.TTNCData(saveObject)
		self.__getAttitudeData = getDriverData.AttitudeData(saveObject)
		self.__tasks = [] #List will be populated with background tasks to cancel them
		self.__safeMode = safeModeObject
		self.__antennaDeployer = BackupAntennaDeployer()
		self.__antennaDoor = AntennaDoor()
		self.__timeToNextWindow = -1


	async def run(self):
		print('Antenna Deploy Running!')
		self.__tasks.append(asyncio.create_task(pythonInterrupt.interrupt()))
		self.__tasks.append(asyncio.create_task(self.__getTTNCData.collectTTNCData(1))) #Antenna deploy is mission mode 1
		self.__tasks.append(asyncio.create_task(self.__getAttitudeData.collectAttitudeData()))
		self.__tasks.append(asyncio.create_task(self.__safeMode.thresholdCheck())) #Check battery conditions, run safe mode if battery drops below safe level
		self.__tasks.append(asyncio.create_task(self.skipToPostBoom()))
		self.__tasks.append(asyncio.create_task(self.transmit()))
		eps=EPS()
		if self.skipToPostBoom():
			return True
		while True: #Runs antenna deploy loop
			if (eps.getBusVoltage()>self.deployVoltage):
				await asyncio.gather(self.__antennaDeployer.deployPrimary()) #Fire Primary Backup Resistor
				doorStatus = self.__antennaDoor.readDoorStatus() #Check Door status
				if doorStatus == (1,1,1,1): #probably need to change this to actually work
					if self.skipToPostBoom():
						return True
					self.cancelAllTasks(self.__tasks)
					print('Doors are open, returning true')
					return True
				else:
					if self.skipToPostBoom():
						return True
					print('Firing secondary, primary did not work. Returning True')
					await asyncio.gather(self.__antennaDeployer.deploySecondary())
					self.cancelAllTasks(self.__tasks)
					return True
			else:
				if self.skipToPostBoom():
					return True
				if(self.timeWaited > self.maximumWaitTime):
					self.__safeMode.run(10) #1 hour
					await asyncio.sleep(5) #This is an artifact of testing, and will not matter for the actual flight software
				else:
					#Wait 1 minute
					print('Waiting 1 minute until battery status resolves')
					self.timeWaited = self.timeWaited+1
					await asyncio.sleep(60)

	async def transmit(self):
		while True:
			print("Inside of first while loop")
			while True:
				print("Inside of second while loop")
				#if close enough, prep files
				#wait until 5 seconds before, return True
				if(self.__timeToNextWindow is not -1 and self.__timeToNextWindow<14): #If next window is in 2 minutes or less
					if(self.__datatype < 3): #Attitude, TTNC, or Deployment data
						prepareFiles.prepareData(self.__duration, self.__datatype, self.__startFromBeginning, self.__index)
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
						subprocess.Popen(["sudo", txisrCodePath, str(self.__datatype)])
						#os.system(txisrCodePath + ' ' + str(self.__datatype) + ' &') #Call TXISR Code
						self.__timeToNextWindow = -1
						break
					else:
						print('Transmission flag is not enabled')
				await asyncio.sleep(0.1) #Check at 10Hz until the window time gap is less than 5 seconds

	def cancelAllTasks(self, taskList):
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")

	async def skipToPostBoom(self):
		print("Inside skipToPostBoom, skipping value is:", packetProcessing.skippingToPostBoom)
		if packetProcessing.skippingToPostBoom:
			self.cancelAllTasks(self.__tasks)
			return True
		else:
			await asyncio.sleep(1)

	async def readNextTransferWindow(self, transferWindowFilename):
		while True:
			print("Inside transfer window.")
			#read the given transfer window file and extract the data for the soonest transfer window
			fileChecker.checkFile(transferWindowFilename)
			transferWindowFile = open(transferWindowFilename)
			sendData = 0
			soonestWindowTime = 0
			for line in transferWindowFile:
				print("reading line: ")
				print(line)
				data = line.split(",")
				print(data)
				#data[0] = time of next window, data[1] = duration of window, data[2] = datatype, data[3] = picture number
				print(float(data[0]), float(data[0]) - time.time(), TRANSFER_WINDOW_BUFFER_TIME)
				if(float(data[0]) - time.time() > TRANSFER_WINDOW_BUFFER_TIME):  #if the transfer window is at BUFFER_TIME milliseconds in the future
					if(soonestWindowTime == 0 or float(data[0]) - time.time() < soonestWindowTime):
						soonestWindowTime = float(data[0]) - time.time()
						sendData = data
						print(sendData)
			if not(sendData == 0):
				#print("Found next transfer window: ")
				#print(sendData)
				self.__timeToNextWindow = float(sendData[0]) - time.time()
				self.__duration = int(sendData[1])
				self.__datatype = int(sendData[2])
				self.__pictureNumber = int(sendData[3])
				self.__nextWindowTime = float(sendData[0])
				self.__startFromBeginning = bool(sendData[4])
				self.__index = int(sendData[5])
				# print(self.__startFromBeginning)
				# print(self.__timeToNextWindow)
				# print(self.__duration)
				# print(self.__datatype)
				# print(self.__pictureNumber)
				# print(self.__index)
			await asyncio.sleep(3) #Checks transmission windows every 10 seconds
