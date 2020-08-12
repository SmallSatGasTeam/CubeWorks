import sys
import time
sys.path.append('../../')
import asyncio
from flightLogic.missionModes import safe
from flightLogic.getDriverData import *
import Drivers.eps.EPS as EPS
from TXISR.interrupt import INTERRUPT

TRANSFER_WINDOW_BUFFER_TIME = 30000

class postBoomMode:
	self.__timeToNextWindow
	self.__duration
	self.__datatype
	self.__pictureNumber
	
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
				
	def readNextTransferWindow(self, transferWindowFilename):
		#read the given transfer window file and extract the data for the soonest transfer window
		transferWindowFile = open(transferWindowFilename)
		sendData = 0
		soonestWindowTime = 0
		for line in transferWindowFile:
			data = line.split(",")
			#data[0] = time of next window, data[1] = duration of window, data[2] = datatype, data[3] = picture number
			if(data[0] - time.time() > TRANSFER_WINDOW_BUFFER_TIME):  #if the transfer window is at BUFFER_TIME milliseconds in the future
				if(soonestWindowTime = 0 or data[0] - time.time() < soonestWindowTime):
					soonestWindowTime = data[0] - time.time()
					sendData = data
		if not(sendData == 0): 
			self.__timeToNextWindow = sendData[0] - time.time()
			self.__duration = sendData[1]
			self.__datatype = sendData[2]
			self.__pictureNumber = sendData[3]
		
			




	def cancellAllTasks(self, taskList): #Isn't used in this class, but here anyways
		try:
			for t in taskList:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("Caught thrown exception in cancelling background task")
