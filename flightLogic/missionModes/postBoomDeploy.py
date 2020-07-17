import asyncio
from safe import safe
import getDriverData
import Drivers.eps.EPS as EPS

class postBoomMode:
	def __init__(self, saveobject):
		postBoomTimeFile = f.open("postBoomTime.txt", "w+")
		self.__getDataTTNC = getDriverData.TTNCData(saveobject)
		self.__getDataAttitude = getDriverData.AttitudeData(saveobject)
	async def run(self):
		#Set up background processes
		ttncData = self.__getDataTTNC.TTNCData()
        attitudeData = self.__getDataAttitude.AttitudeData()
		asyncio.run(ttncData.collectTTNCData(4), attitudeData.collectAttitudeData())#Post-boom is mode 4
		safeMode = safe()
		asyncio.run(safeMode.thresholdCheck())
		
		await while True:
			if not postBoomTimeFile.read(1):
				postBoomTimeFile.write(str(0))#File is empty
			else:
				runningTime = int(postBoomTimeFile.read())
				if runningTime>86400: #Live for more than 24 hours
					postBoomTimeFile.write(str(0))
					postBoomTimeFile.close()
				else: 
					postBoomTimeFile.write(str(runningTime+60))
			await asyncio.sleep(60) #check every 60 seconds if post boom has been running for more than 24 hours
