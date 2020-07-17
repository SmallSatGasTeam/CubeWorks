import asyncio
from safe import safe
from getDriverData import *
import Drivers.boomDeployer.BoomDeployer
import Drivers.camera.Camera

class boomMode:
	def __init__(self, saveobject):
		self.__getDataTTNC = getDriverData.TTNCData(saveobject)
		self.__getDataAttitude = getDriverData.AttitudeData(saveobject)
		self.__getDataDeployData = getDriverData.DeployData()
	async def run(self):
		#Setting up background processes
		ttncData = self.__getDataTTNC.TTNCData()
        attitudeData = self.__getDataAttitude.AttitudeData()
		deployData = getDriverData.DeployData()
		asyncio.run(ttncData.collectTTNCData(3), attitudeData.collectAttitudeData(), deployData.collectDeployData()) #Boom deploy is mode 3
		safeMode = safe()
		asyncio.run(safeMode.thresholdCheck())
		
		#Deploy boom, take picture
		deployer = BoomDeployer()
		cam = Camera()
		deployer.deploy()
		cam.takePicture()
		cam.compressLowResToFiles()
		cam.compressHighResToFiles()
		return True #Go to post-boom deploy
		
