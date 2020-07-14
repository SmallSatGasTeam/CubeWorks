import asyncio
from safe import safe
from getDriverData import *
import Drivers.boomDeployer.BoomDeployer
import Drivers.camera.Camera

class boomMode:
	def __init__(self):
		None
	def run(self):
		#Setting up background processes
		ttncData = TTNCData()
		attitudeData = AttitudeData()
		deployData = DeployData()
		asyncio.run(ttncData.collectTTNCData(), attitudeData.collectAttitudeData(), deployData.collectDeployData())
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
		
