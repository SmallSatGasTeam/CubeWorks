import asyncio
from .safe import safe
from ..getDriverData import *
import Drivers.eps.EPS as EPS

class postBoomMode:
	def __init__(self, saveobject):
		self.postBoomTimeFile = open("postBoomTime.txt", "w+")
		self.__getDataTTNC = TTNCData(saveobject)
		self.__getDataAttitude =  AttitudeData(saveobject)
	async def run(self):
		#Set up background processes
		ttncData = self.__getDataTTNC
		attitudeData = self.__getDataAttitude
		asyncio.run(ttncData.collectTTNCData(4))
		asyncio.run(attitudeData.collectAttitudeData())#Post-boom is mode 4
		safeMode = safe()
		asyncio.run(safeMode.thresholdCheck())
		
		await while True:
			if not self.postBoomTimeFile.read(1):
				self.postBoomTimeFile.write(str(0))#File is empty
			else:
				runningTime = int(self.postBoomTimeFile.read())
				if runningTime>86400: #Live for more than 24 hours
					self.postBoomTimeFile.write(str(0))
					self.postBoomTimeFile.close()
				else: 
					self.postBoomTimeFile.write(str(runningTime+60))
			await asyncio.sleep(60) #check every 60 seconds if post boom has been running for more than 24 hours
