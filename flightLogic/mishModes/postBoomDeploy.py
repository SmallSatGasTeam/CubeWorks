import asyncio
from safe import safe
from getDriverData import *
import Drivers.eps.EPS as EPS

class postBoomMode:
	def __init__(self):
		postBoomTimeFile = f.open("postBoomTime.txt", "w+")
	async def run(self):
		#Set up background processes
		ttncData = TTNCData()
		attitudeData = AttitudeData()
		asyncio.run(ttncData.collectTTNCData(), attitudeData.collectAttitudeData())
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
