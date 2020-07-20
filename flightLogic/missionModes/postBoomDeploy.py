import asyncio
from .safe import safe
from ..getDriverData import *
import Drivers.eps.EPS as EPS

class postBoomMode:
	def __init__(self, saveobject):
		self.postBoomTimeFile = open("postBoomTime.txt", "w+")
		self.__getDataTTNC = TTNCData(saveobject)
		self.__getDataAttitude =  AttitudeData(saveobject)
		self.__tasks = [] # List will be populated with all background tasks
		self.__safeMode = safe()

	async def run(self):
		#Set up background processes
		ttncData = self.__getDataTTNC
		attitudeData = self.__getDataAttitude
		self.__tasks.append(asyncio.create_task(ttncData.collectTTNCData(4))) #Post-boom is mode 4
		self.__tasks.append(asyncio.create_task(attitudeData.collectAttitudeData))
		self.__tasks.append(asyncio.create_task(self.__safeMode.thresholdCheck()))
		self.__tasks.append(asyncio.create_task(self.rebootLoop()))



	async def rebootLoop(self):
		while True:
			upTime = 0
			if upTime>86400: #Live for more than 24 hours
				self.__safeMode.run(1) #restart, powering off Pi for 1 minute
			else:
				upTime += 60
				await asyncio.sleep(60)

	def cancellAllTasks(self, taskList): #Isn't used in this class, but here anyways
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")
