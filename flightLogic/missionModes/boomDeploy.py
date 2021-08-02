import sys
import time
sys.path.append('../../')
import asyncio
from flightLogic.getDriverData import *
import Drivers.boomDeployer as boomDeployer
from TXISR import pythonInterrupt
from TXISR.packetProcessing import packetProcessing as packet
from flightLogic.missionModes.heartBeat import heart_beat

#safeModeObject was deleted below in the init parameters after saveObject
class boomMode:
	def __init__(self, saveObject, transmitObject, cam, packetObj):
		self.__getTTNCData = TTNCData(saveObject)
		self.__getAttitudeData = AttitudeData(saveObject)
		self.__getDeployData = DeployData(saveObject)
		self.__tasks = []  # Empty list will be populated with all background tasks
		# self.__safeMode = safeModeObject
		self.__saveObject = saveObject
		self.__transmit = transmitObject
		self.__packetProcessing = packet(transmitObject, cam)
		self.__heartBeatObj = heart_beat()
		self.__cam = cam
		self.__packetProcessing = packetObj

	async def run(self):
		# Setting up background processes
		self.__tasks.append(asyncio.create_task(self.__heartBeatObj.heartBeatRun()))
		self.__tasks.append(asyncio.create_task(pythonInterrupt.interrupt(self.__transmit, self.__packetProcessing)))
		self.__tasks.append(asyncio.create_task(self.__getTTNCData.collectTTNCData(3)))  # Boom deploy is mode 3
		self.__tasks.append(asyncio.create_task(self.__getAttitudeData.collectAttitudeData()))
		self.__tasks.append(asyncio.create_task(self.__getDeployData.collectDeployData()))

		print("Starting boom deploy")
		# Deploy boom, take picture
		await asyncio.sleep(5)

		deployer = boomDeployer.BoomDeployer()
		await deployer.deploy() 
		

		try:
			print("Taking picture")
			self.__cam.takePicture()
		except Exception as e:
			print("Failed to take a picture because we received excpetion:", repr(e))
		await asyncio.sleep(5)
		# 	await asyncio.sleep(60) #sleep if a transmission is running
		self.cancelAllTasks(self.__tasks) # Cancel all background tasks
		return True  # Go to post-boom deploy

	def cancelAllTasks(self, taskList):
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")
