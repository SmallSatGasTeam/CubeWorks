import sys
import time
sys.path.append('../../')
import asyncio
from flightLogic.missionModes import safe
from flightLogic.getDriverData import *
import Drivers.boomDeployer as boomDeployer
from Drivers.camera import Camera
from TXISR import pythonInterrupt



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

		# Deploy boom, take picture
		await asyncio.sleep(5)
		deployer = boomDeployer.BoomDeployer()
		cam = Camera()
		await deployer.deploy() #From LOGAN: Deployer.deploy is now an asyncio method, run it like the others
		cam.takePicture()
		await asyncio.sleep(5)
		self.cancelAllTasks(self.__tasks) # Cancel all background tasks
		return True  # Go to post-boom deploy

	def cancelAllTasks(self, taskList):
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")
