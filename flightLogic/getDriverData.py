"""
Gets driver data for each data set. Also writes that data to files.
"""

### NOTE NEED TO ADD "ASYNC" TO THE DEF FOR EACH METHOD IN THE DRIVER CLASSES
import sys
sys.path.append('../')
from Drivers import *
import asyncio
from .saveTofiles import *

class TTNCData:
	def __init__(self, saveobject):
		save = saveobject
		self.__data = []

	async def getData(self, missionMode):
		#gets all TTNC data - need to pass in missionMode when calling it
		timestamp = await RTC.read()
		packetType = 1
		mode = missionMode
		reboot_count = reboot #not sure how to do this
		boombox_uv = await UVDriver.read()
		SP_X_Plus_Temp = TempSensor.read() #this returns 2 values but we only want 1 of them
		SP_Z_Plus_Temp = TemoSensor.read() #same comment as above
		piTemp = CpuTemperature.read()
		EPSMCUTemp = EPS.getMCUTemp()
		Cell1Temp = EPS.getCell1Temp()
		Cell2Temp = EPS.getCell2Temp()
		BattVoltage = EPS.getBusVoltage()
		BattCurrent = EPS.getBusCurrent()
		BCRVoltage = EPS.getBCRVoltage()
		BCRCurrent = EPS.getBCRCurrent()
		EPS3V3Current = EPS.get3v3Current()
		EPS5VCurrent = EPS.get5v5Current()
		SP_X_Voltage = EPS.getSPXVoltage()
		SP_X_Plus_Current = EPS.getSPXPlusCurrent()
		SP_X_Minus_Current = EPS.getSPXMinusCurrent()
		SP_Y_Voltage = EPS.getSPYVoltage()
		SP_Y_Plus_Current = EPS.getSPYPlusCurrent()
		SP_Y_Minus_Current = EPS.getSPYMinusCurrent()
		SP_Z_Voltage = EPS.getSPZVoltage()
        	#this is a temp arry to pass the data into the print, this will save the data for later
        	self.__data = [timestamp,packetType, mode, reboot_count, boombox_uv, SP_X_Plus_Temp, SP_Z_Plus_Temp, piTemp, EPSMCUTemp,
            	Cell1Temp, BattVoltage, BCRCurrent, EPS3V3Current, EPS5VCurrent, SP_X_Voltage, SP_X_Plus_Current, SP_X_Minus_Current,
            	SP_Y_Voltage, SP_Y_Plus_Current, SP_Y_Minus_Current , SP_Z_Voltage] 
 		#call the write data methood
        	writeData()
	async def writeData(self):
		#writes all TTNC data to file
        	#this func will save our ttnc data in the corrisponding file
		save.writeTTNC(self.__data)
		
	async def collectTTNCData(self, mMode): #sets up the loop to collect data. Easiest way to do this, since you'll only have to run 1-3 functions in each mission mode
		await while True:
			#Get TTNC data @ 0.0083Hz
			getData(mMode)
			await asyncio.sleep(120)

class DeployData():
	def __init__(self, saveobject):
		save = saveobject
        self.__data2 = []

	async def getData(self):
		#gets all Boom Deployment data
		timestamp = await RTC.read()
		packetType = 2
		boombox_uv = await UVDriver.read()
		accel = await Accelerometer.read() #note this returns the acceleration for all 3 axes in an array. Needs to be split into 3 separate values.
		#save the data for later
        	self.__data2 = [timestamp, packetType, boombox_uv, accel]
        	#call the write func
        	writeData()

	async def writeData(self):
		#writes Boom Deployment data to file
        	save.writeDeploy(self.__data2)
		
	async def collectDeployData(self): #sets up the loop to collect data. Easiest way to do this, since you'll only have to run 1-3 functions in each mission mode
		await while True:
			#Get Deploy data @ 20Hz
			getData()
			await asyncio.sleep(0.05)

class AttitudeData():
	def __init__(self, saveobject):
		save = saveobject
        self.__data3 = []

	async def getData(self):
		#gets all Attitude data
		timestamp = await RTC.read()
		packetType = 0
		sunSensor = sunSensor.read() #note this returns all 5 sun sensor values. Needs to be split into individual values
		mag = Magnetometer.read() #note this returns all 3 mag values. Needs to be split into individual values
        	#save the data for latter
		self.__data3 = [timestamp, packetType, sunSensor, mag]
        	#call the write func 
        	writeData()

	async def writeData(self):
		#writes Attitude Data to file
        	save.writeAttitude(self.__data3) 
		
	async def collectAttitudeData(self): #sets up the loop to collect data. Easiest way to do this, since you'll only have to run 1-3 functions in each mission mode
		await while True:
			#Get Attitude data @ 1Hz
			getData()
			await asyncio.sleep(1)
