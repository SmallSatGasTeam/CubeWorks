import time
import Drivers.backupAntennaDeployer.BackupAntennaDeployer as antennaDeploy
import Drivers.antennaDoor.AntennaDoor as antennaStatus
import Drivers.eps.EPS as EPS
import asyncio
from .safe import safe
from ..getDriverData import *


class antennaMode:

    def __init__(self, saveobject):
        self.deployVoltage = 5 #Threshold voltage to deploy
        self.maximumWaitTime = 30 #Maximum time to wait for deployment before going to SAFE
        self.timeWaited = 0 #Time already waited - zero
        self.__getDataTTNC = getDriverData.TTNCData(saveobject)
	self.__getDataAttitude = getDriverData.AttitudeData(saveobject)
	self.__tasks = [] #List will be populated with background tasks to cancel them

    async def run(self):
        ttncData = self.__getDataTTNC
        attitudeData = self.__getDataAttitude
        self.__tasks.append(asyncio.create_task(ttncData.collectTTNCData(1)) #asyncio.run is exclusive, 
        asyncio.run(attitudeData.collectAttitudeData()) #Antenna Deploy is mission mode 1
        safeMode = safe()

	asyncio.run(safeMode.thresholdCheck()) #Check battery conditions, run safe mode if battery drops below safe level 

	async def deployAntenna(self):
		#Perform tasks for antenna deployment
		eps=EPS()
        	await while True:
	 		if (eps.getBusVoltage()>self.deployVoltage):
                	antennaDeploy.deploy()
                	if doorStatus == (0,0,0,0): #probably need to change this to actually work
                    		#Doors are open, cancel all tasks and then 
                    		return True
            		else:
                		if(self.timeWaited > self.maximumWaitTime):
                    			safeMode.run(10) #1 hour
                		else:
                    			#Wait 1 minute
                    			self.timeWaited = self.timeWaited+1
                    			await asyncio.sleep(60)
	
	def cancellAllTasks(self, taskList):
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")
