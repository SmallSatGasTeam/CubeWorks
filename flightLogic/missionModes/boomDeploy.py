import sys
import time
sys.path.append('../../')
import asyncio
from flightLogic.getDriverData import *
import Drivers.boomDeployer as boomDeployer
from Drivers.camera import Camera
from TXISR import pythonInterrupt
from TXISR.packetProcessing import packetProcessing as packet
from DummyDrivers.boomDeployer.BoomDeployer import BoomDeployer as DummyBoomDeployer

DONTMURDERBEN = False
#safeModeObject was deleted below in the init parameters after saveObject
class boomMode:
	def __init__(self, saveObject, transmitObject):
		self.__getTTNCData = TTNCData(saveObject)
		self.__getAttitudeData = AttitudeData(saveObject)
		self.__getDeployData = DeployData(saveObject)
		self.__tasks = []  # Empty list will be populated with all background tasks
		# self.__safeMode = safeModeObject
		self.__saveObject = saveObject
		self.__transmit = transmitObject
		self.__packetProcessing = packet(transmitObject)

	async def run(self):
		# Setting up background processes
		self.__tasks.append(asyncio.create_task(pythonInterrupt.interrupt(self.__transmit)))
		self.__tasks.append(asyncio.create_task(self.__getTTNCData.collectTTNCData(3)))  # Boom deploy is mode 3
		self.__tasks.append(asyncio.create_task(self.__getAttitudeData.collectAttitudeData()))
		self.__tasks.append(asyncio.create_task(self.__getDeployData.collectDeployData()))
		# self.__tasks.append(asyncio.create_task(self.__safeMode.thresholdCheck()))
		self.__tasks.append(asyncio.create_task(self.skipToPostBoom()))
		self.__tasks.append(asyncio.create_task(self.__transmit.readNextTransferWindow()))
		self.__tasks.append(asyncio.create_task(self.__transmit.getReadyForWindows()))
		self.__tasks.append(asyncio.create_task(self.__transmit.upDateTime()))

		print("Starting boom deploy")
		# Deploy boom, take picture
		if await self.skipToPostBoom():
			return True
		await asyncio.sleep(5)
		if DONTMURDERBEN:
			deployer = DummyBoomDeployer()
		else:
			deployer = boomDeployer.BoomDeployer()
		cam = Camera()
		await deployer.deploy() #From LOGAN: Deployer.deploy is now an asyncio method, run it like the others
		
		if await self.skipToPostBoom():
			return True

		try:
			print("Taking picture")
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
		"""
		Skips to postBoomDeploy mode if the command is received from the ground
		station.
		"""
		print("Inside skipToPostBoom, skipping value is:", self.__packetProcessing.skip())
		if self.__packetProcessing.skip():
			self.cancelAllTasks(self.__tasks)
			return True
		else:
			await asyncio.sleep(1)