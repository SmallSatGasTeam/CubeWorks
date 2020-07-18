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
	async def run(self):
		#Setting up background processes
		ttncData = self.__getDataTTNC
		attitudeData = self.__getDataAttitude
		deployData = DeployData()
		asyncio.run(ttncData.collectTTNCData(3), attitudeData.collectAttitudeData(), deployData.collectDeployData())  # Boom deploy is mode 3
		safeMode = safe()
		asyncio.run(safeMode.thresholdCheck())
		
		# Deploy boom, take picture
		deployer = boomDeployer.BoomDeployer()
		cam = camera.Camera()
		deployer.deploy()
		cam.takePicture()
		cam.compressLowResToFiles()
		cam.compressHighResToFiles()
		return True  # Go to post-boom deploy
