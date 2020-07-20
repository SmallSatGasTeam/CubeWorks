import asyncio
from .safe import safe
from ..getDriverData import *
import Drivers.eps.EPS as EPS
import Drivers.sunSensors.sunSensorDriver as sunSensorDriver


class preBoomMode:
	def __init__(self, saveobject):
		self.thresholdVoltage = 5 #Threshold voltage to deploy AeroBoom.
		self.criticalVoltage = 3.3 #Critical voltage, below this go to SAFE
		self.darkVoltage = 1 #Average voltage from solar panels that, if below this, indicates GASPACS is in darkness
		self.darkMinutes = 5 #How many minutes GASPACS must be on the dark side for before moving forward
		self.lightMinimumMinutes = 5 #Minimum amount of time GASPACS must be on light side of orbit before deploying
		self.lightMaximumMinutes = 60 #Maximum amount of time GASPACS may be on light side of orbit before deploying, must be less than 90 by a fair margin since less than half of orbit can be sun
		self.batteryStatusOk = False
		self.maximumWaitTime = 240 #Max time GASPACS can wait, charging batteries, before SAFEing
		self.timeWaited = 0
		self.sunlightData = []
		self.__getDataTTNC = TTNCData(saveobject)
		self.__getDataAttitude = AttitudeData(saveobject)
		self.__tasks = [] #Will be populated with tasks

	async def run(self):
		ttncData = self.__getDataTTNC
		attitudeData = self.__getDataAttitude
		safeMode = safe()
		self.__tasks.append(asyncio.create_task(ttncData.collectTTNCData(2))) #Pre-Boom is mode 2
		self.__tasks.append(asyncio.create_task(attitudeData.collectAttitudeData()))
		self.__tasks.append(asyncio.create_task(safeMode.thresholdCheck()))
		self.__tasks.append(asyncio.create_task(self.sunCheck()))
		self.__tasks.append(asyncio.create_task(self.lightStatusCheck()))
		self.__tasks.append(asyncio.create_task(self.batteryCheck()))



	async def sunCheck(self):
		sunSensor = sunSensorDriver()
		while True: #Monitor the sunlight, record it in list NOTE: could be improved to halve calls
			vList = sunSensor.read()
			averageVoltage = sum(vList)/len(vList)
			await asyncio.sleep(5)
			averageVoltage = sum(vList)/len(vList)
			self.sunlightData.append(averageVoltage/2)
			await asyncio.sleep(5) #Every 10 seconds, record average solar panel voltage. Rough running average with two pieces to avoid jumps in avg. voltage

	async def lightStatusCheck(self):
		while True: #iterate through array, checking for set amount of dark minutes, then set amount of light minutes no greater than the maximum. When light minutes are greater than the maximum, empties array
			i=0
			darkLength = 0
			lastDark = 0
			while i < len(self.sunlightData): #Loop through sunlightData, checking for X minutes of darkness
				if(self.sunlightData[i]<self.darkVoltage):
					darkLength+=1 #It was in the dark for the 10 seconds recorded in the ith position of sunlightData
				else:
					darkLength = 0 #Maybe darkLength -=1 to avoid damage from one bad measurement? Maybe a smoother running average?
				if(darkLength>self.darkMinutes*6): #If GASPACS has been in dark longer than the preset amount
					lastDark = i
					break
				i+=1
			if lastDark != 0: #Condition from previous while loop has  been met
				q=lastDark
				lightLength = 0
				while q < len(self.sunlightData):
					if(self.sunlightData[q]>=self.darkVoltage):
						lightLength+=1
					else:
						lightLength = 0 #Maybe lightLength -=1 to avoid 1 bad measurement resetting everything
					if(lightLength>self.lightMaximumMinutes*6): #Has been in the light for too long
						self.sunlightData.clear() #Reset array of data
						break
					if(lightLength>self.lightMinimumMinutes*6 and self.batteryStatusOk==True):
						self.cancelAllTasks(self.__tasks) #Cancel all background processes
						return True #Go on to Boom Deploy Mode if the battery is Ok
					q += 1
			await asyncio.sleep(15) #Run this whole while loop every 15 seconds

	async def batteryCheck(self):
		eps = EPS()
		while True: #Checking the battery voltage to see if it's ready for deployment, if it is too low for too long --> SAFE
			if (eps.getBusVoltage()>self.thresholdVoltage):
				self.batteryStatusOk=True
			else:
				self.batteryStatusOk=False
				if(self.timeWaited*12 > self.maximumWaitTime): #5 seconds every wait
					safeMode.run(10) #1 hour
				else:
					#Wait 5 more seconds
					self.timeWaited = self.timeWaited+1
					await asyncio.sleep(5) #Check battery every 5 seconds

	def cancellAllTasks(self, taskList): #Isn't used in this class, but here anyways
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")
