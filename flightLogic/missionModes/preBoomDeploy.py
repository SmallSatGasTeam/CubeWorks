import sys
sys.path.append('../../')
import asyncio
from flightLogic.missionModes import safe
from flightLogic.getDriverData import *
from Drivers.eps import EPS as EPS
from Drivers.sunSensors import sunSensorDriver as sunSensorDriver
from TXISR import pythonInterrupt


class preBoomMode:
	def __init__(self, saveObject, safeModeObject):
		self.thresholdVoltage = 3.5 #Threshold voltage to deploy AeroBoom.
		self.criticalVoltage = 3.1 #Critical voltage, below this go to SAFE
		self.darkVoltage = .1 #Average voltage from sunsors that, if below this, indicates GASPACS is in darkness
		self.darkMinutes = .1 #How many minutes GASPACS must be on the dark side for before moving forward
		self.lightMinimumMinutes = .1 #Minimum amount of time GASPACS must be on light side of orbit before deploying
		self.lightMaximumMinutes = 60 #Maximum amount of time GASPACS may be on light side of orbit before deploying, must be less than 90 by a fair margin since less than half of orbit can be sun
		self.batteryStatusOk = False
		self.maximumWaitTime = 240 #Max time GASPACS can wait, charging batteries, before SAFEing
		self.timeWaited = 0
		self.sunlightData = []
		self.__getTTNCData = TTNCData(saveObject)
		self.__getAttitudeData = AttitudeData(saveObject)
		self.__tasks = [] #Will be populated with tasks
		self.__saveOject = saveObject
		self.__safeMode = safeModeObject

	async def run(self):
		self.__tasks.append(asyncio.create_task(pythonInterrupt.interrupt()))
		self.__tasks.append(asyncio.create_task(self.__getTTNCData.collectTTNCData(2))) #Pre-Boom is mode 2
		self.__tasks.append(asyncio.create_task(self.__getAttitudeData.collectAttitudeData()))
		self.__tasks.append(asyncio.create_task(self.__safeMode.thresholdCheck()))
		self.__tasks.append(asyncio.create_task(self.sunCheck()))
		self.__tasks.append(asyncio.create_task(self.batteryCheck()))
		while True: #iterate through array, checking for set amount of dark minutes, then set amount of light minutes no greater than the maximum. When light minutes are greater than the maximum, empties array
			i=0
			darkLength = 0
			lastDark = 0
			#print(self.sunlightData)
			while i < len(self.sunlightData): #Loop through sunlightData, checking for X minutes of darkness
				if(self.sunlightData[i]<self.darkVoltage):
					darkLength+=1 #It was in the dark for the 5 seconds recorded in the ith position of sunlightData
					index = i
				else:
					if(darkLength>self.darkMinutes*12):
						lastDark = i
						break
					darkLength = 0 #Maybe darkLength -=1 to avoid damage from one bad measurement? Maybe a smoother running average?
				i+=1


			print('Last Dark ' + str(lastDark))

			if lastDark != 0: #Condition from previous while loop has  been met
				q=lastDark
				lightLength = 0
				print("Now looking for min minutes of Sunlight")
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
						print('Returning and exiting')
						return True #Go on to Boom Deploy Mode if the battery is Ok
					q += 1
			await asyncio.sleep(5) #Run this whole while loop every 15 seconds

	async def sunCheck(self):
		sunSensor = sunSensorDriver.sunSensor()
		while True: #Monitor the sunlight, record it in list NOTE: could be improved to halve calls
			vList = sunSensor.read()
			self.sunlightData.append(max(vList))
			await asyncio.sleep(5)

	async def batteryCheck(self):
		eps = EPS()
		while True: #Checking the battery voltage to see if it's ready for deployment, if it is too low for too long --> SAFE
			if (eps.getBusVoltage()>self.thresholdVoltage):
				print('Battery above threshold voltage for deployment')
				self.batteryStatusOk=True
				self.timeWaited = 0
				await asyncio.sleep(5)
			else:
				self.batteryStatusOk=False

				if(self.timeWaited*12 > self.maximumWaitTime): #5 seconds every wait
						self.safeMode.run(10) #1 hour
						print('Battery too low for too long. Rebooting')
						self.timeWaited = 0
						await asyncio.sleep(5)
				else:
					#Wait 5 more seconds
					self.timeWaited = self.timeWaited+1
					await asyncio.sleep(5) #Check battery every 5 seconds

	def cancelAllTasks(self, taskList): #Isn't used in this class, but here anyways
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")
