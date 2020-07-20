import time
import Drivers.backupAntennaDeployer.BackupAntennaDeployer as antennaDeploy
import Drivers.antennaDoor.AntennaDoor as antennaStatus
import Drivers.eps.EPS as EPS
import asyncio
from .safe import safe
import flightLogic.getDriverData as getDriverData


class antennaMode:

	def __init__(self, saveobject):
		self.deployVoltage = 5 #Threshold voltage to deploy
		self.maximumWaitTime = 30 #Maximum time to wait for deployment before going to SAFE
		self.timeWaited = 0 #Time already waited - zero
		self.__getDataTTNC = getDriverData.TTNCData(saveobject)
		self.__getDataAttitude = getDriverData.AttitudeData(saveobject)
		self.__tasks = [] #List will be populated with background tasks to cancel them
		self.__safeMode = safe()


	async def run(self):
		ttncData = self.__getDataTTNC
		attitudeData = self.__getDataAttitude
		self.__tasks.append(asyncio.create_task(ttncData.collectTTNCData(1))) #Antenna deploy is mission mode 1
		self.__tasks.append(asyncio.create_task(attitudeData.collectAttitudeData()))
		self.__tasks.append(asyncio.create_task(self.__safeMode.thresholdCheck())) #Check battery conditions, run safe mode if battery drops below safe level
		self.__tasks.append(asyncio.create_task(self.deployAntenna())) #Runs Antenna deploy loop

	async def deployAntenna(self):
		#Perform tasks for antenna deployment
		eps=EPS()
		while True:
			if (eps.getBusVoltage()>self.deployVoltage):
				antennaDeploy.deploy()
				doors = antennaStatus()
				doorStatus = doors.readDoorStatus()
				if doorStatus == (0,0,0,0): #probably need to change this to actually work
					#Doors are open, cancel all tasks and then
					return True
				else:
					if(self.timeWaited > self.maximumWaitTime):
						self.__safeMode.run(10) #1 hour
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
