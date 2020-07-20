import asyncio
from .safe import safe
from ..getDriverData import *
import Drivers.boomDeployer.BoomDeployer as boomDeployer
import Drivers.camera.Camera as camera

class boomMode:
	def __init__(self, saveobject):
		self.__getDataTTNC = TTNCData(saveobject)
		self.__getDataAttitude = AttitudeData(saveobject)
		self.__getDataDeployData = DeployData()
		self.__tasks = [] # Empty list will be populated with all background tasks

	async def run(self):
		#Setting up background processes
		ttncData = self.__getDataTTNC
		attitudeData = self.__getDataAttitude
		deployData = DeployData()
		safeMode = safe()

		self.__tasks.append(asyncio.create_task(ttncData.collectTTNCData(3))) #Boom deploy is mode 3
		self.__tasks.append(asyncio.create_task(attitudeData.collectAttitudeData()))
		self.__tasks.append(asyncio.create_task(deployData.collectDeployData()))
		self.__tasks.append(asyncio.create_task(safeMode.thresholdCheck()))

		# Deploy boom, take picture
		deployer = boomDeployer.BoomDeployer()
		cam = camera.Camera()
		deployer.deploy()
		cam.takePicture()
		cam.compressLowResToFiles()
		cam.compressHighResToFiles()
		self.cancelAllTasks(self.__tasks) # Cancel all background tasks
		return True  # Go to post-boom deploy

	def cancellAllTasks(self, taskList):
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")

