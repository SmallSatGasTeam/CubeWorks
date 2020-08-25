"""
Gets driver data for each data set. Also writes that data to files.
"""
import asyncio
import sys
import os
sys.path.append('../')
import DummyDrivers as Drivers
import struct
import flightLogic.saveTofiles as saveTofiles



gaspacsBytes = str(b'GASPACS'.hex())

def readBootCount():
	try:
		dataFile = open(os.path.dirname(__file__) + '/bootRecords')
		return int(dataFile.readline().rstrip())
	except:
		try:
			dataFileBackup = open(os.path.dirname(__file__) + '/backupBootRecords')
			return int(dataFileBackup.readline().rstrip())
		except:
			print('Double file exception - are both files non-existent?')

class TTNCData:
	def __init__(self, saveobject):
		self.__save = saveobject
		self.__ttncData = None
		self.EPS = Drivers.eps.EPS()
		self.UVDriver = Drivers.UV.UVDriver()
		self.RTC = Drivers.rtc.RTC()
		self.CpuTempSensor = Drivers.cpuTemperature.CpuTemperature()
		self.TempSensor = Drivers.solarPanelTemp.TempSensor()

	async def getData(self, missionMode):
		packet = ''
		# gets all TTNC data - need to pass in missionMode when calling it
		timestamp = int4tohex(self.RTC.readSeconds())
		packetType = int1tohex(1)
		mode = int1tohex(missionMode)
		reboot_count = int2tohex(readBootCount())
		#No need for await on these, since they're not sleeping
		boombox_uv = float4tohex(self.UVDriver.read())
		SP_X_Plus_Temp, SP_Z_Plus_Temp = self.TempSensor.read()
		SP_X_Plus_Temp = float4tohex(SP_X_Plus_Temp)
		SP_Z_Plus_Temp = float4tohex(SP_Z_Plus_Temp)
		piTemp = float4tohex(self.CpuTempSensor.read())
		EPSMCUTemp = float4tohex(self.EPS.getMCUTemp())
		Cell1Temp = float4tohex(self.EPS.getCell1Temp())
		Cell2Temp = float4tohex(self.EPS.getCell2Temp())
		BattVoltage = float4tohex(self.EPS.getBusVoltage())
		BattCurrent = float4tohex(self.EPS.getBusCurrent())
		BCRVoltage = float4tohex(self.EPS.getBCRVoltage())
		BCRCurrent = float4tohex(self.EPS.getBCRCurrent())
		EPS3V3Current = float4tohex(self.EPS.get3V3Current())
		EPS5VCurrent = float4tohex(self.EPS.get5VCurrent())
		SP_X_Voltage = float4tohex(self.EPS.getSPXVoltage())
		SP_X_Plus_Current = float4tohex(self.EPS.getSPXPlusCurrent())
		SP_X_Minus_Current = float4tohex(self.EPS.getSPXMinusCurrent())
		SP_Y_Voltage = float4tohex(self.EPS.getSPYVoltage())
		SP_Y_Plus_Current = float4tohex(self.EPS.getSPYPlusCurrent())
		SP_Y_Minus_Current = float4tohex(self.EPS.getSPYMinusCurrent())
		SP_Z_Voltage = float4tohex(self.EPS.getSPZVoltage())

		packet += gaspacsBytes + packetType + timestamp + mode + reboot_count + boombox_uv + SP_X_Plus_Temp + SP_Z_Plus_Temp + piTemp + EPSMCUTemp + Cell1Temp + BattVoltage + BCRCurrent + EPS3V3Current + EPS5VCurrent + SP_X_Voltage + SP_X_Plus_Current + SP_X_Minus_Current + SP_Y_Voltage + SP_Y_Plus_Current + SP_Y_Minus_Current + SP_Z_Voltage + gaspacsBytes

		packetTimestamp = str(int(self.RTC.readSeconds())).zfill(10)+':'
		packet = packetTimestamp + packet
		self.__ttncData = packet

	async def writeData(self):
		#writes TTNC data array to file
		await self.__save.writeTTNC(self.__ttncData)

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
		self.__deployData = None
		self.Accelerometer = Drivers.Accelerometer()

	async def getData(self):
		#gets all Boom Deployment data
		packet = ''
		timestamp = int8tohex(self.RTC.readMilliseconds())
		packetType = int1tohex(2)
		boombox_uv = float4tohex(self.UVDriver.read())
		accelX, accelY, accelZ = self.Accelerometer.read()
		accelX = float4tohex(accelX)
		accelY = float4tohex(accelY)
		accelZ = float4tohex(accelZ)
		packet = ''
		packet += gaspacsBytes + packetType + timestamp + boombox_uv + accelX + accelY + accelZ
		packetTimestamp = str(int(self.RTC.readSeconds())).zfill(10)+':'
		packet = packetTimestamp + packet
		self.__deployData = packet

	async def writeData(self):
		#writes Boom Deployment data array to file
		await self.__save.writeDeploy(self.__deployData)

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
		self.__attitudeData = None
		self.sunSensor = Drivers.sunSensors.sunSensorDriver.sunSensor()
		self.Magnetometer = Drivers.Magnetometer()

	async def getData(self):
		#gets all Attitude data
		packet = ''
		timestamp = int4tohex(self.RTC.readSeconds())
		packetType = int1tohex(0)
		allSunSensors = self.sunSensor.read()
		sunSensor1, sunSensor2, sunSensor3, sunSensor4, sunSensor5 = [allSunSensors[i] for i in range(5)]
		sunSensor1 = float4tohex(sunSensor1)
		sunSensor2 = float4tohex(sunSensor2)
		sunSensor3 = float4tohex(sunSensor3)
		sunSensor4 = float4tohex(sunSensor4)
		sunSensor5 = float4tohex(sunSensor5)

		mag1, mag2, mag3 = self.Magnetometer.read()
		mag1 = float4tohex(mag1)
		mag2 = float4tohex(mag2)
		mag3 = float4tohex(mag3)

		packet += gaspacsBytes + packetType + timestamp + sunSensor1 + sunSensor2 + sunSensor3 + sunSensor4 + sunSensor5 + mag1 + mag2 + mag3 + gaspacsBytes
		packetTimestamp = str(int(self.RTC.readSeconds())).zfill(10)+':'
		packet = packetTimestamp + packet
		self.__attitudeData = packet

	async def writeData(self):
		#writes Attitude Data array to file
		await self.save.writeAttitude(self.__attitudeData)

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

def float4tohex(num):
	#takes a 4 byte float, returns a hex representation of it
	return str(hex(struct.unpack('<I', struct.pack('<f', num))[0]))[2:]

def int4tohex(num):
	#takes a 4 byte int, returns a hex representation of it
	return str(format(num, '08x'))[-8:]

def int1tohex(num):
	#takes a 1 byte integer, returns a hex representation of it
	return str(format(num, '02x'))[-2:]

def int2tohex(num):
	#takes a 2 byte integer, returns a hex representation of it
	return str(format(num, '04x'))[-4:]

def int8tohex(num):
	#takes an 8 byte integer, returns a hex representation of it
	return str(format(num, '016x'))[-16:]
