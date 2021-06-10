import sys
sys.path.append('../../')
import asyncio
from flightLogic.getDriverData import *
from TXISR import pythonInterrupt


REBOOT_WAIT_TIME = 900 #15 minutes, 900 seconds

"safeModeObject was deleted below in the init parameters after saveObject"
class postBoomMode:
	def __init__(self, saveObject, transmitObject):
		self.__transmit = transmitObject
		self.__getTTNCData = TTNCData(saveObject)
		self.__getAttitudeData =  AttitudeData(saveObject)
		self.__tasks = [] # List will be populated with all background tasks
		# self.__safeMode = safeModeObject
		print("Initialized postBoomDeploy")

	async def run(self):
		#Set up background processes
		print("Inside of run in postBoomDeploy")
		self.__tasks.append(asyncio.create_task(pythonInterrupt.interrupt(self.__transmit)))
		self.__tasks.append(asyncio.create_task(self.__getTTNCData.collectTTNCData(4))) #Post-boom is mode 4
		self.__tasks.append(asyncio.create_task(self.__getAttitudeData.collectAttitudeData()))
		# self.__tasks.append(asyncio.create_task(self.__safeMode.thresholdCheck()))
		self.__tasks.append(asyncio.create_task(self.__transmit.readNextTransferWindow()))
		self.__tasks.append(asyncio.create_task(self.__transmit.transmit()))
		self.__tasks.append(asyncio.create_task(self.__transmit.upDateTime()))
		
		print("Initalized all tasks.")
		while True:
			#Don't remove this print statement, the while loop is an integral part
			# of making sure that postBoomDeploy doesn't crash and it needs to
			# have something in there so it doesn't crash and suffer
			print('This is post Boom Deploy')
			await asyncio.sleep(10)	

	def cancellAllTasks(self, taskList): #Isn't used in this class, but here anyways
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")
