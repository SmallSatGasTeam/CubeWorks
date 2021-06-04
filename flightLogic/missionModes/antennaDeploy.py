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



class antennaMode:
	"""
	Deploys the antenna when the battery voltage is high enough.
	Instantiated in mainFlightLogic.
	"""

	def __init__(self, saveObject, safeModeObject, transmitObject):
		self.deployVoltage = 3 #Threshold voltage to deploy
		self.maximumWaitTime = 30 #Maximum time to wait for deployment before going to SAFE
		self.timeWaited = 0 #Time already waited - zero
		self.__getTTNCData = getDriverData.TTNCData(saveObject)
		self.__getAttitudeData = getDriverData.AttitudeData(saveObject)
		self.__tasks = [] #List will be populated with background tasks to cancel them
		self.__safeMode = safeModeObject
		self.__antennaDeployer = BackupAntennaDeployer()
		self.__antennaDoor = AntennaDoor()
		self.__transmit = transmitObject
		self.__packetProcessing = packet(transmitObject)


	async def run(self):
		"""
		Deploys the antenna when the battery voltage is high enough.
		Runs async tasks pythonInterrupt, collectTTNCData, collectAttitudeData,
		thresholdcheck, skipToPostBoom, readNextTransferWindow, trasmit
		"""
		print('Antenna Deploy Running!')
		self.__tasks.append(asyncio.create_task(pythonInterrupt.interrupt(self.__transmit)))
		self.__tasks.append(asyncio.create_task(self.__getTTNCData.collectTTNCData(1))) #Antenna deploy is mission mode 1
		self.__tasks.append(asyncio.create_task(self.__getAttitudeData.collectAttitudeData()))
		self.__tasks.append(asyncio.create_task(self.__safeMode.thresholdCheck())) #Check battery conditions, run safe mode if battery drops below safe level
		self.__tasks.append(asyncio.create_task(self.skipToPostBoom()))
		self.__tasks.append(asyncio.create_task(self.__transmit.readNextTransferWindow()))
		self.__tasks.append(asyncio.create_task(self.__transmit.transmit()))
		
		eps=EPS()
		#If ground station has sent command to skip to post boom
		# if await self.skipToPostBoom():
		# 	return True	#Finish this mode and move on
		while True: #Runs antenna deploy loop
			if (eps.getBusVoltage()>self.deployVoltage): #If the bus voltage is high enough
				await asyncio.gather(self.__antennaDeployer.deployPrimary()) #Fire Primary Backup Resistor
				doorStatus = self.__antennaDoor.readDoorStatus() #Check Door status
				if doorStatus == (1,1,1,1): #NOTE: probably need to change this to actually work
					#If ground station has sent command to skip to post boom					
					if await self.skipToPostBoom():
						return True #Finish this mode and move on
					self.cancelAllTasks(self.__tasks)
					print('Doors are open, returning true')
					return True
				else:
					#If ground station has sent command to skip to post boom
					if await self.skipToPostBoom():
						return True #Finish this mode and move on
					print('Firing secondary, primary did not work. Returning True')
					await asyncio.gather(self.__antennaDeployer.deploySecondary())
					self.cancelAllTasks(self.__tasks)
					return True
			else:
				#If ground station has sent command to skip to post boom
				if await self.skipToPostBoom():
					return True #Finish this mode and move on
				if(self.timeWaited > self.maximumWaitTime):
					self.__safeMode.run(10) #1 hour
					await asyncio.sleep(5) #This is an artifact of testing, and will not matter for the actual flight software
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

	async def skipToPostBoom(self):
		"""
		Skips to postBoomDeploy mode if the command is received from the ground
		station.
		"""
		print("Inside skipToPostBoom, skipping value is:", self.__packetProcessing.skip())
		#If the command has been received to skip to postBoom
		if self.__packetProcessing.skip():
			self.cancelAllTasks(self.__tasks) #Cancel all tasks
			return True #Finish this mode and move on
		else:
			await asyncio.sleep(1)