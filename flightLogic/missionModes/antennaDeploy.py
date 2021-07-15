"""
Contains the antennaMode class and the functions: run, cancelAllTasks, and
skipToPostBoom
"""
import sys
#import subprocess
import os
sys.path.append('../../')
import time
from Drivers.backupAntennaDeployer import BackupAntennaDeployer
from Drivers.antennaDoor import AntennaDoor
import Drivers.eps.EPS as EPS
import asyncio
import flightLogic.getDriverData as getDriverData
from TXISR import pythonInterrupt
from TXISR.packetProcessing import packetProcessing as packet
from flightLogic.missionModes.heartBeat import heart_beat
from inspect import currentframe, getframeinfo

getBusVoltageMin = 3.5
getBusVoltageMax = 5.1

class antennaMode:
	"""
	Deploys the antenna when the battery voltage is high enough.
	Instantiated in mainFlightLogic.
	"""
	"safeModeObject was deleted below in the init parameters after saveObject"
	def __init__(self, saveObject, transmitObject, packetObj):
		self.deployVoltage = 3 #Threshold voltage to deploy
		self.maximumWaitTime = 30 #Maximum time to wait for deployment before going to SAFE
		self.timeWaited = 0 #Time already waited - zero
		self.__getTTNCData = getDriverData.TTNCData(saveObject)
		self.__getAttitudeData = getDriverData.AttitudeData(saveObject)
		self.__tasks = [] #List will be populated with background tasks to cancel them
		# self.__safeMode = safeModeObject
		self.__antennaDeployer = BackupAntennaDeployer()
		self.__antennaDoor = AntennaDoor()
		self.__transmit = transmitObject
		self.__packetProcessing = packetObj
		self.__heartBeatObj = heart_beat()


	async def run(self):
		"""
		Deploys the antenna when the battery voltage is high enough.
		Runs async tasks pythonInterrupt, collectTTNCData, collectAttitudeData,
		thresholdcheck, skipToPostBoom, readNextTransferWindow, trasmit
		"""
		print('Antenna Deploy Running!')
		self.__tasks.append(asyncio.create_task(self.__heartBeatObj.heartBeatRun()))
		self.__tasks.append(asyncio.create_task(pythonInterrupt.interrupt(self.__transmit, self.__packetProcessing)))
		self.__tasks.append(asyncio.create_task(self.__getTTNCData.collectTTNCData(1))) #Antenna deploy is mission mode 1
		self.__tasks.append(asyncio.create_task(self.__getAttitudeData.collectAttitudeData()))

		
		eps=EPS()
		#If ground station has sent command to skip to post boom
		# if await self.skipToPostBoom():
		# 	return True	#Finish this mode and move on
		while True: #Runs antenna deploy loop
			try:
				BusVoltage = eps.getBusVoltage()
				if(BusVoltage < getBusVoltageMin) | (BusVoltage > getBusVoltageMax):
					raise unexpectedValue
			except Exception as e:
				BusVoltage = 4.18
				print("Failed to retrieve BusVoltage, got", BusVoltage)
			if (BusVoltage >self.deployVoltage): #If the bus voltage is high enough
				await asyncio.gather(self.__antennaDeployer.deployPrimary()) #Fire Primary Backup Resistor
				doorStatus = self.__antennaDoor.readDoorStatus() #Check Door status
				if doorStatus == (1,1,1,1): #NOTE: probably need to change this to actually work
					#If ground station has sent command to skip to post boom			
					self.cancelAllTasks(self.__tasks)
					print('Doors are open, returning true')
					return True
				else:
					print('Firing secondary, primary did not work. Returning True')
					await asyncio.gather(self.__antennaDeployer.deploySecondary())
					self.cancelAllTasks(self.__tasks)
					return True
			else:
				if(self.timeWaited > self.maximumWaitTime):
					await asyncio.gather(self.__antennaDeployer.deployPrimary()) #Fire Primary Backup Resistor
					doorStatus = self.__antennaDoor.readDoorStatus() #Check Door status
					if doorStatus == (1,1,1,1): #NOTE: probably need to change this to actually work	
						# Dont cancel task until we are done transmitting		
						self.cancelAllTasks(self.__tasks)
						print('Doors are open, returning true')
						return True
					else:
						print('Firing secondary, primary did not work. Returning True')
						await asyncio.gather(self.__antennaDeployer.deploySecondary())
						# Dont cancel task until we are done transmitting
						self.cancelAllTasks(self.__tasks)
						return True
				else:
					#Wait 1 minute
					print('Waiting 1 minute until battery status resolves')
					self.timeWaited = self.timeWaited+1
					await asyncio.sleep(60)

	def cancelAllTasks(self, taskList):
		"""
		Cancels all async tasks created at the beginning of run.
		"""
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")
