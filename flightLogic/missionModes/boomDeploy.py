import sys
import time
sys.path.append('../../')
import asyncio
from flightLogic.missionModes import safe
from flightLogic.getDriverData import *
import Drivers.boomDeployer as boomDeployer
#import Drivers.camera.Camera as camera
from TXISR.interrupt import INTERRUPT



class boomMode:
	def __init__(self, saveobject):
		self.__getDataTTNC = TTNCData(saveobject)
		self.__getDataAttitude = AttitudeData(saveobject)
		self.__getDataDeployData = DeployData(saveobject)
		self.__tasks = []  # Empty list will be populated with all background tasks
		self.safeMode = safe.safe(saveobject)
		self.saveobject = saveobject

	async def run(self):
		# Setting up background processes
		ttncData = self.__getDataTTNC
		attitudeData = self.__getDataAttitude
		deployData = DeployData(self.saveobject)
		interruptObject = INTERRUPT()
		self.__tasks.append(asyncio.create_task(interruptObject.watchTxWindows()))
		self.__tasks.append(asyncio.create_task(interruptObject.watchReceptions()))
		self.__tasks.append(asyncio.create_task(ttncData.collectTTNCData(3)))  # Boom deploy is mode 3
		self.__tasks.append(asyncio.create_task(attitudeData.collectAttitudeData()))
		self.__tasks.append(asyncio.create_task(deployData.collectDeployData()))
		self.__tasks.append(asyncio.create_task(self.safeMode.thresholdCheck()))
		self.__tasks.append(asyncio.create_task(self.safeMode.heartBeat()))

		# Deploy boom, take picture
		await asyncio.sleep(5)
		deployer = boomDeployer.BoomDeployer()
		#cam = camera.Camera()
		await deployer.deploy() #From LOGAN: Deployer.deploy is now an asyncio method, run it like the others
		#cam.takePicture()
		#cam.compressLowResToFiles()
		#cam.compressHighResToFiles()
		self.cancelAllTasks(self.__tasks) # Cancel all background tasks
		await asyncio.sleep(5)
		return True  # Go to post-boom deploy

	def cancelAllTasks(self, taskList):
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")
