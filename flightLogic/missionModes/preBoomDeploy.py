import sys
sys.path.append('../../')
import asyncio
from flightLogic.getDriverData import *
from Drivers.eps import EPS as EPS
from Drivers.sunSensors import sunSensorDriver
from TXISR import pythonInterrupt

from inspect import currentframe, getframeinfo
from TXISR.packetProcessing import packetProcessing as packet
from flightLogic.missionModes.heartBeat import heart_beat


sunSensorMin = 0.0
sunSensorMax = 3.3
getBusVoltageMin = 3.5
getBusVoltageMax = 5.1


DEBUG = False

#safeModeObject was deleted below in the init parameters after saveObject
class preBoomMode:
	def __init__(self, saveObject, transmitObject, packetObj):
		self.thresholdVoltage = 3.85 #Threshold voltage to deploy AeroBoom.
		self.darkVoltage = 0.9 #Average voltage from sunsors that, if below this, indicates GASPACS is in darkness
		self.lightMinimumMinutes = 1 #Minimum amount of time GASPACS must be on light side of orbit before deploying
		self.batteryStatusOk = False
		self.sunlightData = 0
		self.__getTTNCData = TTNCData(saveObject)
		self.__getAttitudeData = AttitudeData(saveObject)
		self.__tasks = [] #Will be populated with tasks
		self.__packetProcessing = packetObj
		self.__transmit = transmitObject
		self.__heartBeatObj = heart_beat()


	async def run(self):
		self.__tasks.append(asyncio.create_task(self.__heartBeatObj.heartBeatRun()))
		self.__tasks.append(asyncio.create_task(pythonInterrupt.interrupt(self.__transmit, self.__packetProcessing)))
		self.__tasks.append(asyncio.create_task(self.__getTTNCData.collectTTNCData(2))) #Pre-Boom is mode 2
		self.__tasks.append(asyncio.create_task(self.__getAttitudeData.collectAttitudeData()))
		self.__tasks.append(asyncio.create_task(self.sunCheck()))
		self.__tasks.append(asyncio.create_task(self.batteryCheck()))

		"""This code was intended to find out when to deploy the boom based on how long GASPACS was in the light. 
		This was commented out because there is no need for this functionality if there is no resin in the boom"""
		while True:
			print("checking for sunlight")

			if ((self.sunlightData > self.darkVoltage) and self.batteryStatusOk == True):
				self.cancelAllTasks(self.__tasks) #Cancel all background processes, this depolys the boom basically
				print('Returning and exiting')
				return True #Go on to Boom Deploy Mode if the battery is Ok
			await asyncio.sleep(5) #Run this whole while loop every 15 seconds

	async def sunCheck(self):
		sunSensor = sunSensorDriver.sunSensor()
		while True: #Monitor the sunlight, record it in list NOTE: could be improved to halve calls
			vList = [0.0, 0.0, 0.0, 0.0, 0.0]
			try:
				vList = sunSensor.read()
				if DEBUG:
					print("Pre boom deploy sun sensor values: ", vList)
				size = 0
				while size < 5:
					if (vList[size] < sunSensorMin) or (vList[size] > sunSensorMax):
				 		raise unexpectedValue
					size += 1
			except Exception as e:
				print("Failure to pull sunSensor data. Received error:", repr(e),
				getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
				vList[0] = 1

			self.sunlightData = max(vList)
			await asyncio.sleep(5)

	async def batteryCheck(self):
		eps = EPS()
		while True: #Checking the battery voltage to see if it's ready for deployment, if it is too low for too long --> SAFE
			try:
				BusVoltage = eps.getBusVoltage()
				#NOTE: This line is for testing! DO NOT 
				if(BusVoltage < getBusVoltageMin) or (BusVoltage > getBusVoltageMax):
					raise unexpectedValue
			except Exception as e:
				BusVoltage = 4.18
				print("Failed to retrieve BusVoltage, got", BusVoltage, "instead. Received error: ", 
				repr(e), getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			
			if (BusVoltage > self.thresholdVoltage):
				print('Battery above threshold voltage for deployment')
				self.batteryStatusOk=True
				await asyncio.sleep(5)
			else:
				self.batteryStatusOk=False

			#Wait 5 more seconds
			await asyncio.sleep(5) #Check battery every 5 seconds

	def cancelAllTasks(self, taskList): #Isn't used in this class, but here anyways
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")

class unexpectedValue(Exception):
	print("Received unexpected value.")
	pass
