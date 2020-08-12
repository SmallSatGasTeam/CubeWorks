"""
Gets driver data for each data set. Also writes that data to files.
"""
import asyncio
import sys
sys.path.append('../')
import Drivers
import struct
import flightLogic.saveTofiles as saveTofiles

def float4tohex(num):
	#takes a 4 byte float, returns a hex representation of it
	return str(hex(struct.unpack('<I', struct.pack('<f', num))[0]))[2:]

def int4tohex(num):
	#takes a 4 byte int, returns a hex representation of it
	return str(format(num, '16x'))

def int1tohex(num):
	#takes a 1 byte integer, returns a hex representation of it
	pass

def int2tohex(num):
	#takes a 2 byte integer, returns a hex representation of it
	pass

class TTNCData:
	def __init__(self, saveobject):
		self.__save = saveobject
		self.__ttncDataArray = []
		self.EPS = Drivers.eps.EPS()
		self.UVDriver = Drivers.UV.UVDriver()
		self.RTC = Drivers.rtc.RTC()
		self.CpuTempSensor = Drivers.cpuTemperature.CpuTemperature()
		self.TempSensor = Drivers.solarPanelTemp.TempSensor()

	async def getData(self, missionMode):
		# gets all TTNC data - need to pass in missionMode when calling it
		timestamp = self.RTC.read()
		packetType = 1
		mode = missionMode
		reboot_count = 0  #TODO This needs to read in from Shawn's file
		#No need for await on these, since they're not sleeping
		boombox_uv = self.UVDriver.read()
		SP_X_Plus_Temp, SP_Z_Plus_Temp = self.TempSensor.read()
		piTemp = self.CpuTempSensor.read()
		EPSMCUTemp = self.EPS.getMCUTemp()
		Cell1Temp = self.EPS.getCell1Temp()
		Cell2Temp = self.EPS.getCell2Temp()
		BattVoltage = self.EPS.getBusVoltage()
		BattCurrent = self.EPS.getBusCurrent()
		BCRVoltage = self.EPS.getBCRVoltage()
		BCRCurrent = self.EPS.getBCRCurrent()
		EPS3V3Current = self.EPS.get3V3Current()
		EPS5VCurrent = self.EPS.get5VCurrent()
		SP_X_Voltage = self.EPS.getSPXVoltage()
		SP_X_Plus_Current = self.EPS.getSPXPlusCurrent()
		SP_X_Minus_Current = self.EPS.getSPXMinusCurrent()
		SP_Y_Voltage = self.EPS.getSPYVoltage()
		SP_Y_Plus_Current = self.EPS.getSPYPlusCurrent()
		SP_Y_Minus_Current = self.EPS.getSPYMinusCurrent()
		SP_Z_Voltage = self.EPS.getSPZVoltage()

		#Save the data into an array
		self.__ttncDataArray = [timestamp, packetType, mode, reboot_count, boombox_uv, SP_X_Plus_Temp, SP_Z_Plus_Temp, piTemp, EPSMCUTemp,
				Cell1Temp, BattVoltage, BCRCurrent, EPS3V3Current, EPS5VCurrent, SP_X_Voltage, SP_X_Plus_Current, SP_X_Minus_Current,
				SP_Y_Voltage, SP_Y_Plus_Current, SP_Y_Minus_Current , SP_Z_Voltage]

	async def writeData(self):
		#writes TTNC data array to file
		await self.__save.writeTTNC(self.__ttncDataArray)

	async def collectTTNCData(self, mMode):
		# Data collection loop
		while True:
			# Get TTNC data
			await self.getData(mMode)
			# Write data to file
			print("getting TTNC data")
			await self.writeData()
			# Sleep for 120 seconds (0.0083 Hz)
			await asyncio.sleep(120)

class DeployData():
	def __init__(self, saveobject):
		self.__save = saveobject
		self.RTC = Drivers.rtc.RTC()
		self.UVDriver = Drivers.UV.UVDriver()
		self.__deployDataArray = []
		self.Accelerometer = Drivers.Accelerometer()

	async def getData(self):
		#gets all Boom Deployment data
		timestamp = self.RTC.read()
		packetType = 2
		boombox_uv = self.UVDriver.read()
		accelX, accelY, accelZ = self.Accelerometer.read()

		#save the data into an array
		self.__deployDataArray = [timestamp, packetType, boombox_uv, accelX, accelY, accelZ]

	async def writeData(self):
		#writes Boom Deployment data array to file
		await self.__save.writeDeploy(self.__deployDataArray)

	async def collectDeployData(self):
		# Data collection loop
		while True:
			# Get Deploy data
			await self.getData()
			# Write data to file
			await self.writeData()
			print("getting deployment data")
			# Sleep for 50 ms (20Hz)
			await asyncio.sleep(0.05)

class AttitudeData():
	def __init__(self, saveobject):
		self.save = saveobject
		self.RTC = Drivers.rtc.RTC()
		self.attitudeDataArray = []
		self.sunSensor = Drivers.sunSensors.sunSensorDriver.sunSensor()
		self.Magnetometer = Drivers.Magnetometer()

	async def getData(self):
		#gets all Attitude data
		timestamp = self.RTC.read()
		packetType = 0
		sunSensor1, sunSensor2, sunSensor3, sunSensor4, sunSensor5 = self.sunSensor.read()
		mag1, mag2, mag3 = self.Magnetometer.read()

		#save the data into an array
		self.attitudeDataArray = [timestamp, packetType, sunSensor1, sunSensor2, sunSensor3, sunSensor4, sunSensor5, mag1, mag2, mag3]

	async def writeData(self):
		#writes Attitude Data array to file
		await self.save.writeAttitude(self.attitudeDataArray)

	async def collectAttitudeData(self):
		# Data collection loop
		while True:
			# Get Attitude data
			await self.getData()
			# Write data to file
			await self.writeData()
			print("getting attitude data")
			# Sleep for 1 second (1 Hz)
			await asyncio.sleep(1)


