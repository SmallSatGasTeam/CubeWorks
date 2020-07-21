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
		self.__ttncDataArray = []

	async def getData(self, missionMode):
		# gets all TTNC data - need to pass in missionMode when calling it
		timestamp = await RTC.read()
		packetType = 1
		mode = missionMode
		reboot_count = reboot #not sure how to do this
		boombox_uv = await UVDriver.read()
		SP_X_Plus_Temp, SP_Z_Plus_Temp = await TempSensor.read()
		piTemp = await CpuTemperature.read()
		EPSMCUTemp = await EPS.getMCUTemp()
		Cell1Temp = await EPS.getCell1Temp()
		Cell2Temp = await EPS.getCell2Temp()
		BattVoltage = await EPS.getBusVoltage()
		BattCurrent = await EPS.getBusCurrent()
		BCRVoltage = await EPS.getBCRVoltage()
		BCRCurrent = await EPS.getBCRCurrent()
		EPS3V3Current = await EPS.get3v3Current()
		EPS5VCurrent = await EPS.get5v5Current()
		SP_X_Voltage = await EPS.getSPXVoltage()
		SP_X_Plus_Current = await EPS.getSPXPlusCurrent()
		SP_X_Minus_Current = await EPS.getSPXMinusCurrent()
		SP_Y_Voltage = await EPS.getSPYVoltage()
		SP_Y_Plus_Current = await EPS.getSPYPlusCurrent()
		SP_Y_Minus_Current = await EPS.getSPYMinusCurrent()
		SP_Z_Voltage = await EPS.getSPZVoltage()

		#Save the data into an array
			self.__ttncDataArray = [timestamp, packetType, mode, reboot_count, boombox_uv, SP_X_Plus_Temp, SP_Z_Plus_Temp, piTemp, EPSMCUTemp,
				Cell1Temp, BattVoltage, BCRCurrent, EPS3V3Current, EPS5VCurrent, SP_X_Voltage, SP_X_Plus_Current, SP_X_Minus_Current,
				SP_Y_Voltage, SP_Y_Plus_Current, SP_Y_Minus_Current , SP_Z_Voltage]

	async def writeData(self):
		#writes TTNC data array to file
		save.writeTTNC(self.__ttncDataArray)

	async def collectTTNCData(self, mMode):
		# Data collection loop
		await while True:
			# Get TTNC data
			getData(mMode)
			# Write data to file
			writeData()
			# Sleep for 120 seconds (0.0083 Hz)
			await asyncio.sleep(120)

class DeployData():
	def __init__(self, saveobject):
		save = saveobject
			self.__deployDataArray = []

	async def getData(self):
		#gets all Boom Deployment data
		timestamp = await RTC.read()
		packetType = 2
		boombox_uv = await UVDriver.read()
		accelX, accelY, accelZ = await Accelerometer.read()

		#save the data into an array
			self.__deployDataArray = [timestamp, packetType, boombox_uv, accelX, accelY, accelZ]

	async def writeData(self):
		#writes Boom Deployment data array to file
			save.writeDeploy(self.__deployDataArray)

	async def collectDeployData(self):
		# Data collection loop
		await while True:
			# Get Deploy data
			getData()
			# Write data to file
			writeData()
			# Sleep for 50 ms (20Hz)
			await asyncio.sleep(0.05)

class AttitudeData():
	def __init__(self, saveobject):
		save = saveobject
			self.__attitudeDataArray = []

	async def getData(self):
		#gets all Attitude data
		timestamp = await RTC.read()
		packetType = 0
		sunSensor1, sunSensor2, sunSensor3, sunSensor4, sunSensor5 = sunSensor.read()
		mag1, mag2, mag3 = Magnetometer.read()

		#save the data into an array
		self.__attitudeDataArray = [timestamp, packetType, sunSensor1, sunSensor2, sunSensor3, sunSensor4, sunSensor5, mag1, mag2, mag3]

	async def writeData(self):
		#writes Attitude Data array to file
			save.writeAttitude(self.__attitudeDataArray)

	async def collectAttitudeData(self):
		# Data collection loop
		await while True:
			# Get Attitude data
			getData()
			# Write data to file
			writeData()
			# Sleep for 1 second (1 Hz)
			await asyncio.sleep(1)
