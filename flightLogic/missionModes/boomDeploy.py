import sys
import time
sys.path.append('../../')
import asyncio
from flightLogic.missionModes import safe
from flightLogic.getDriverData import *
import Drivers.boomDeployer as boomDeployer
from Drivers.camera import Camera
from TXISR import pythonInterrupt
from TXISR import packetProcessing

TRANSFER_WINDOW_BUFFER_TIME = 10 #30 seconds

class boomMode:
	def __init__(self, saveObject, safeModeObject):
		self.__getTTNCData = TTNCData(saveObject)
		self.__getAttitudeData = AttitudeData(saveObject)
		self.__getDeployData = DeployData(saveObject)
		self.__tasks = []  # Empty list will be populated with all background tasks
		self.__safeMode = safeModeObject
		self.__saveObject = saveObject

	async def run(self):
		# Setting up background processes
		self.__tasks.append(asyncio.create_task(pythonInterrupt.interrupt()))
		self.__tasks.append(asyncio.create_task(self.__getTTNCData.collectTTNCData(3)))  # Boom deploy is mode 3
		self.__tasks.append(asyncio.create_task(self.__getAttitudeData.collectAttitudeData()))
		self.__tasks.append(asyncio.create_task(self.__getDeployData.collectDeployData()))
		self.__tasks.append(asyncio.create_task(self.__safeMode.thresholdCheck()))
		self.__tasks.append(asyncio.create_task(self.skipToPostBoom()))

		# Deploy boom, take picture
		if self.skipToPostBoom():
			return True
		await asyncio.sleep(5)
		deployer = boomDeployer.BoomDeployer()
		cam = Camera()
		await deployer.deploy() #From LOGAN: Deployer.deploy is now an asyncio method, run it like the others
		
		if self.skipToPostBoom():
			return True

		try:
			cam.takePicture()
		except Exception as e:
			print("Failed to take a picture because we received excpetion:", repr(e))
		await asyncio.sleep(5)
		self.cancelAllTasks(self.__tasks) # Cancel all background tasks
		return True  # Go to post-boom deploy

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
