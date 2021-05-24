import sys
sys.path.append('../../')
import asyncio
from flightLogic.getDriverData import *
from Drivers.eps import EPS as EPS
from Drivers.sunSensors import sunSensorDriver
"""DO NOT PUSH LINE 9 TO MASTER! THIS IS FOR TESTING PURPOSES ONLY."""
from DummyDrivers.sunSensors import sunSensorDriver as DummySunSensorDriver
from TXISR import pythonInterrupt
from inspect import currentframe, getframeinfo
from TXISR import packetProcessing


sunSensorMin = 0.0
sunSensorMax = 3.3
getBusVoltageMin = 3.5
getBusVoltageMax = 5.1


DummySunSensor = True
DEBUG = False


class preBoomMode:
	def __init__(self, saveObject, safeModeObject, transmitObject):
		self.thresholdVoltage = 3.5 #Threshold voltage to deploy AeroBoom.
		self.criticalVoltage = 3.1 #Critical voltage, below this go to SAFE
		self.darkVoltage = .1 #Average voltage from sunsors that, if below this, indicates GASPACS is in darkness
		self.darkMinutes = .2 #How many minutes GASPACS must be on the dark side for before moving forward
		self.lightMinimumMinutes = 1 #Minimum amount of time GASPACS must be on light side of orbit before deploying
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
		self.__transmit = transmitObject

	async def run(self):
		self.__tasks.append(asyncio.create_task(pythonInterrupt.interrupt()))
		self.__tasks.append(asyncio.create_task(self.__getTTNCData.collectTTNCData(2))) #Pre-Boom is mode 2
		self.__tasks.append(asyncio.create_task(self.__getAttitudeData.collectAttitudeData()))
		self.__tasks.append(asyncio.create_task(self.__safeMode.thresholdCheck()))
		self.__tasks.append(asyncio.create_task(self.sunCheck()))
		self.__tasks.append(asyncio.create_task(self.batteryCheck()))
		self.__tasks.append(asyncio.create_task(self.__transmit.readNextTransferWindow()))
		self.__tasks.append(asyncio.create_task(self.__transmit.transmit()))

		while True: #iterate through array, checking for set amount of dark minutes, then set amount of light minutes no greater than the maximum. When light minutes are greater than the maximum, empties array
			if await self.skipToPostBoom():
				print("Exiting postBoomDeploy through skipToPostBoom")
				return True
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
			if DEBUG:
				print("Dark Length: ", darkLength)


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

					if(lightLength>self.lightMaximumMinutes*12): #Has been in the light for too long
						self.sunlightData.clear() #Reset array of data
						break
					if(lightLength>self.lightMinimumMinutes*12 and self.batteryStatusOk==True):
						self.cancelAllTasks(self.__tasks) #Cancel all background processes
						print('Returning and exiting')
						return True #Go on to Boom Deploy Mode if the battery is Ok
					q += 1
				if DEBUG:
					print("Light length: ", lightLength)
			await asyncio.sleep(5) #Run this whole while loop every 15 seconds

	async def sunCheck(self):
		"""DO NOT PUSH THIS IF STATEMENT TO MASTER. THIS IS FOR TESTING PURPOSES ONLY"""
		if DummySunSensor:
			sunSensor = DummySunSensorDriver.sunSensor()
		else:
			sunSensor = sunSensorDriver.sunSensor()
		while True: #Monitor the sunlight, record it in list NOTE: could be improved to halve calls
			try:
				vList = [0.0, 0.0, 0.0, 0.0, 0.0]
				vList = sunSensor.read()
				if DEBUG:
					print("Pre boom deploy sun sensor values: ", vList)
				size = 0
				while size < 5:
					if (vList[size] < sunSensorMin) | (vList[size] > sunSensorMax):
				 		raise unexpectedValue
					size += 1
			except Exception as e:
				print("Failure to pull sunSensor data. Received error:", repr(e),
				getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
				vList[0] = sunSensorMax + 1

			self.sunlightData.append(max(vList))
			await asyncio.sleep(5)

	async def batteryCheck(self):
		eps = EPS()
		while True: #Checking the battery voltage to see if it's ready for deployment, if it is too low for too long --> SAFE
			try:
				BusVoltage = eps.getBusVoltage()
				if(BusVoltage < getBusVoltageMin) | (BusVoltage > getBusVoltageMax):
					raise unexpectedValue
			except Exception as e:
				BusVoltage = 4.18
				print("Failed to retrieve BusVoltage, got", BusVoltage, "instead. Received error: ", 
				repr(e), getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			
			if (BusVoltage > self.thresholdVoltage):
				print('Battery above threshold voltage for deployment')
				self.batteryStatusOk=True
				self.timeWaited = 0
				await asyncio.sleep(5)
			else:
				self.batteryStatusOk=False

				if(self.timeWaited*12 > self.maximumWaitTime): #5 seconds every wait
						self.__safeMode.run(10) #1 hour
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
	
	async def skipToPostBoom(self):
		print("Inside skipToPostBoom, skipping value is:", packetProcessing.skippingToPostBoom)
		if packetProcessing.skippingToPostBoom:
			self.cancelAllTasks(self.__tasks)
			return True
		else:
			await asyncio.sleep(1)

class unexpectedValue(Exception):
	print("Received unexpected value.")
	pass