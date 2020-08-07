import sys
sys.path.append('../../')
import asyncio
from flightLogic.DummymissionModes import safe
from flightLogic.DummygetDriverData import *
import Drivers.eps.DummyEPS as EPS
#from TXISR.interrupt import INTERRUPT

class postBoomMode:
	def __init__(self, saveobject):
		self.postBoomTimeFile = open("postBoomTime.txt", "w+")
		self.__getDataTTNC = TTNCData(saveobject)
		self.__getDataAttitude =  AttitudeData(saveobject)
		self.__tasks = [] # List will be populated with all background tasks
		self.__safeMode = safe.safe(saveobject)

	async def run(self):
		#Set up background processes
		ttncData = self.__getDataTTNC
		attitudeData = self.__getDataAttitude
		interruptObject = INTERRUPT()
		self.__tasks.append(asyncio.create_task(interruptObject.watchTxWindows()))
		self.__tasks.append(asyncio.create_task(interruptObject.watchReceptions()))
		self.__tasks.append(asyncio.create_task(ttncData.collectTTNCData(4))) #Post-boom is mode 4
		self.__tasks.append(asyncio.create_task(attitudeData.collectAttitudeData()))
		self.__tasks.append(asyncio.create_task(self.__safeMode.thresholdCheck()))
		self.__tasks.append(asyncio.create_task(self.__safeMode.heartBeat()))
		upTime = 86100
		while True: #Runs reboot loop
			if upTime>86400: #Live for more than 24 hours
				self.__safeMode.run(1) #restart, powering off Pi for 1 minute
				print('Rebooting raspberry pi')
				upTime = 0 # Won't be necessary for flight article
			else:
				print('Uptime: '+str(upTime))
				await asyncio.sleep(60)
				upTime += 60




	def cancellAllTasks(self, taskList): #Isn't used in this class, but here anyways
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")
