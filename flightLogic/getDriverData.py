"""
Gets driver data for each data set. Also writes that data to files.
"""
import asyncio
import sys
import os
sys.path.append('../')
import Drivers
import struct
import flightLogic.saveTofiles as saveTofiles
from protectionProticol.fileProtection import FileReset
from datetime import datetime
from inspect import currentframe, getframeinfo

fileChecker = FileReset()

gaspacsBytes = str(b'GASPACS'.hex())

"""
All of the minimum and maximum values are listed here. If values from
the sensors/drivers are outside of the valid range, we return exceptions
as error statements.
"""

SP_Plus_TempMin = -40.0
SP_Plus_TempMax = 155.0
piTempMin = 0.0
piTempMax = 70.0
EPSMCUMin = -40
EPSMCUMax = 155
Cell1TempMin = -40.0
Cell1TempMax = 155.0
Cell2TempMin = -40.0
Cell2TempMax = 155.0
BattVoltageMin = 3.5
BattVoltageMax = 5.1
BattCurrentMin = 0.0
BattCurrentMax = 9.0
BCRVoltageMin = 0.0
BCRVoltageMax = 5.1
BCRCurrentMin = 0
BCRCurrentMax = .875
SP_VoltageMin = 0.0
SP_VoltageMax = 5.5
SP_Plus_CurrentMin = 0.0
SP_Plus_CurrentMax = 1.8
SP_Minus_CurrentMin = 0.0
SP_Minus_CurrentMax = 1.8
boombox_uvMin = 0.0
boombox_uvMax = 3.3
accelMin = -16
accelMax = 16
EPS3V3CurrentMin = 0.0 
EPS3V3CurrentMax = 3.0
EPS5VCurrentMin = 0.0
EPS5VCurrentMax = 3.0
sunSensorMin = 0.0
sunSensorMax = 3.3
RTCMin = 0
RTCMax = 4294967295
RTCMinMil = 0
RTCMaxMil = 4294967295 * 1000
magnetometerMin = -100
magnetometerMax = 100

def readBootCount():
	try:
		fileChecker.checkFile('/home/pi/flightLogicData/bootRecords.txt')
		dataFile = open('/home/pi/flightLogicData/bootRecords.txt')
		return int(dataFile.readline().rstrip())
	except:
		try:
			fileChecker.checkFile('/home/pi/flightLogicData/backupBootRecords.txt')
			dataFileBackup = open('/home/pi/flightLogicData/backupBootRecords.txt')
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
		try:
			timestamp = int4tohex(self.RTC.readSeconds())
			if (self.RTC.readSeconds() < RTCMin) or (self.RTC.readSeconds() > RTCMax):
				raise unexpectedValue
		except Exception as e:
			print("Failure to create timestamp. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			timestamp = int4tohex(0000000000)
		
		packetType = int1tohex(1)
		mode = int1tohex(missionMode)
		reboot_count = int2tohex(readBootCount())
		#No need for await on these, since they're not sleeping
		try:
			boombox_uv_Int = self.UVDriver.read()
			boombox_uv = float4tohex(boombox_uv_Int)
			if (boombox_uv_Int < boombox_uvMin) or (boombox_uv_Int > boombox_uvMax):
				print("boombox_uv: ", boombox_uv, "boombox_uv_Int: ", boombox_uv_Int)
				raise unexpectedValue
		except Exception as e:
			# add redundant UVDriver TRY/EXCEPT
			# if no drivers can be called, continue with exception
			print ("failed to return boombox_uv. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			boombox_uv = float4tohex(boombox_uvMax + 1)

		try:
			SP_X_Plus_Temp, SP_Z_Plus_Temp = self.TempSensor.read() 
			if ((SP_X_Plus_Temp < SP_Plus_TempMin) or (SP_X_Plus_Temp > SP_Plus_TempMax) or
			 (SP_Z_Plus_Temp < SP_Plus_TempMin) or (SP_Z_Plus_Temp > SP_Plus_TempMax)):
				raise unexpectedValue
		except Exception as e:
			# add redundant TempSensor TRY/EXCEPT
			# if no drivers can be called, continue with exception
			print("Failed to retrieve temp sensor. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_X_Plus_Temp = SP_Plus_TempMax + 1
			SP_Z_Plus_Temp = SP_Plus_TempMax + 1

		SP_X_Plus_Temp = float4tohex(SP_X_Plus_Temp)
		SP_Z_Plus_Temp = float4tohex(SP_Z_Plus_Temp)

		try:
			piTempInt = self.CpuTempSensor.read()
			piTemp = float4tohex(piTempInt)
			if (piTempInt < piTempMin) or (piTempInt > piTempMax):
				print("piTempInt: ", piTempInt,"piTemp: ", piTemp)
				raise unexpectedValue
		except Exception as e:
			# add redundant CpuTempSensor TRY/EXCEPT
			# if no drivers can be called, continue with exception
			print("Failed to retrieve cpuTempSensor. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			piTemp = float4tohex(piTempMax + 1)

		try:
			EPSMCUTempInt = self.EPS.getMCUTemp()
			EPSMCUTemp = float4tohex(EPSMCUTempInt)
			if ((EPSMCUTempInt < EPSMCUMin) or (EPSMCUTempInt > EPSMCUMax)):
				print("unexpected value eps mcu temp: ", EPSMCUTempInt)
				print(EPSMCUTemp)
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve EPSMCUTemp. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			EPSMCUTemp = float4tohex(EPSMCUMax + 1)

		try:
			Cell1TempInt = self.EPS.getCell1Temp()
			Cell1Temp = float4tohex(Cell1TempInt)
			if ((Cell1TempInt < Cell1TempMin) or (Cell1TempInt > Cell1TempMax)):
				print(Cell1Temp)
				print("Unexpected value recieved from cell temp 1: ", Cell1TempInt)
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve Cell1Temp. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			Cell1Temp = float4tohex(Cell1TempMax + 1)

		try:
			Cell2TempInt = self.EPS.getCell2Temp()
			Cell2Temp = float4tohex(Cell2TempInt)
			if ((Cell2TempInt < Cell2TempMin) or (Cell2TempInt > Cell2TempMax)):
				print(Cell2Temp)
				print("unexpected value recieved from cell temp 2: ", Cell2TempInt)
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve Cell2Temp. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			Cell2Temp = float4tohex(Cell2TempMax + 1)

		try:
			print("BattVoltage: ", self.EPS.getBusVoltage())
			BattVoltageInt = self.EPS.getBusVoltage()
			BattVoltage = float4tohex(BattVoltageInt)
			if ((BattVoltageInt < BattVoltageMin) or (BattVoltageInt > BattVoltageMax)):
				print("BattVoltageInt: ", BattVoltageInt, "BattVoltage: ", BattVoltage)
				raise unexpectedValue
		except Exception as e:
			BattVoltage = float4tohex(BattVoltageMax + 1)
			print("failed to retrieve BattVoltage. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno,
			"Received: ", BattVoltage)

		try:
			BattCurrentInt = self.EPS.getBusCurrent()
			BattCurrent = float4tohex(BattCurrentInt)
			if (BattCurrentInt < BattCurrentMin) or (BattCurrentInt > BattCurrentMax):
				print("BattCurrentInt: ", BattCurrentInt, "BattCurrent: ", BattCurrent)
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve BattCurrent. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			BattCurrent = float4tohex(BattCurrentMax + 1)

		try:
			print("getDriverData: ", self.EPS.getBCRVoltage())
			BCRVoltageInt = self.EPS.getBCRVoltage()
			BCRVoltage = float4tohex(BCRVoltageInt)
			if ((BCRVoltageInt < BCRVoltageMin) or (BCRVoltageInt > BCRVoltageMax)):
				print("BCRVoltageInt: ", BCRVoltageInt, "BCRVoltage: ", BCRVoltage)
				raise unexpectedValue
		except Exception as e:
			BCRVoltage = float4tohex(BCRVoltageMax + 1)
			print("failed to retrieve BCRVoltage. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno, 
			"Received: ", BCRVoltage)

		try:
			BCRCurrentInt = self.EPS.getBCRCurrent()
			BCRCurrent = float4tohex(BCRCurrentInt)
			if (BCRCurrentInt < BCRCurrentMin) or (BCRCurrentInt > BCRCurrentMax):
				print("BCRCurrentInt: ", BCRCurrentInt, "BCRCurrent: ", BCRCurrent)
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve BCRCurrent. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			BCRCurrent = float4tohex(BCRCurrentMax + 1)

		try:
			EPS3V3CurrentInt = self.EPS.get3V3Current()
			EPS3V3Current = float4tohex(EPS3V3CurrentInt)
			if (EPS3V3CurrentInt < EPS3V3CurrentMin) or (EPS3V3CurrentInt > EPS3V3CurrentMax):
				print("EPS3V3CurrentInt: ", EPS3V3CurrentInt, "EPS3V3Current: ", EPS3V3Current)
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve EPS3V3Current. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			EPS3V3Current = float4tohex(EPS3V3CurrentMax + 1)

		try:
			EPS5VCurrentInt = self.EPS.get5VCurrent()
			EPS5VCurrent = float4tohex(EPS5VCurrentInt)
			if (EPS5VCurrentInt < EPS5VCurrentMin) or (EPS5VCurrentInt > EPS5VCurrentMax):
				print("EPS5VCurrentInt:", EPS5VCurrentInt, "EPS5VCurrent: ", EPS5VCurrent )
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve EPS5VCurrent. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			EPS5VCurrent = float4tohex(EPS5VCurrentMax + 1)

		try:
			SP_X_VoltageInt = self.EPS.getSPXVoltage()
			SP_X_Voltage = float4tohex(SP_X_VoltageInt)
			if (SP_X_VoltageInt < SP_VoltageMin) or (SP_X_VoltageInt > SP_VoltageMax):
				print("SP_X_VoltageInt: ", SP_X_VoltageInt, "SP_X_Voltage: ", SP_X_Voltage)
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve SP_X_Voltage. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_X_Voltage = float4tohex(SP_VoltageMax + 1)

		try:
			SP_X_Plus_CurrentInt = self.EPS.getSPXPlusCurrent()
			SP_X_Plus_Current = float4tohex(SP_X_Plus_CurrentInt)
			if (SP_X_Plus_CurrentInt < SP_Plus_CurrentMin) or (SP_X_Plus_CurrentInt > SP_Plus_CurrentMax):
				print("SP_X_Plus_CurrentInt: ", SP_X_Plus_CurrentInt, "SP_X_Plus_Current: ", SP_X_Plus_Current)
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve SP_X_Plus_Current. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_X_Plus_Current = float4tohex(SP_Plus_CurrentMax + 1)

		try:
			SP_X_Minus_CurrentInt = self.EPS.getSPXMinusCurrent()
			SP_X_Minus_Current = float4tohex(SP_X_Minus_CurrentInt)
			if (SP_X_Minus_CurrentInt < SP_Minus_CurrentMin) or (SP_X_Minus_CurrentInt > SP_Minus_CurrentMax):
				print("SP_X_Minus_CurrentInt: ", SP_X_Minus_CurrentInt, "SP_X_Minus_Current: ", SP_X_Minus_Current)
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve SP_X_Minus_Current. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_X_Minus_Current = float4tohex(SP_Minus_CurrentMax + 1)

		try:
			SP_Y_VoltageInt = self.EPS.getSPYVoltage()
			SP_Y_Voltage = float4tohex(SP_Y_VoltageInt)
			if (SP_Y_VoltageInt < SP_VoltageMin) or (SP_Y_VoltageInt > SP_VoltageMax):
				print("SP_Y_VoltageInt: ", SP_Y_VoltageInt, "SP_Y_Voltage", SP_Y_Voltage)
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve SP_Y_Voltage. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_Y_Voltage = float4tohex(SP_VoltageMax + 1)

		try:
			SP_Y_Plus_CurrentInt = self.EPS.getSPYPlusCurrent()
			SP_Y_Plus_Current = float4tohex(SP_Y_Plus_CurrentInt)
			if (SP_Y_Plus_CurrentInt < SP_Plus_CurrentMin) or (SP_Y_Plus_CurrentInt > SP_Plus_CurrentMax):
				print("SP_Y_Plus_CurrentInt: ", SP_Y_Plus_CurrentInt, "SP_Y_Plus_Current: ", SP_Y_Plus_Current)
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve SP_Y_Plus_Current. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_Y_Plus_Current = float4tohex(SP_Plus_CurrentMax + 1)

		try:
			SP_Y_Minus_CurrentInt = self.EPS.getSPYMinusCurrent()
			SP_Y_Minus_Current = float4tohex(SP_Y_Minus_CurrentInt)
			if(SP_Y_Minus_CurrentInt < SP_Minus_CurrentMin) or (SP_Y_Minus_CurrentInt > SP_Minus_CurrentMax):
				print("SP_Y_Minus_CurrentInt: ", SP_Y_Minus_CurrentInt, "SP_Y_Minus_Current: ", SP_Y_Minus_Current)
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve SP_Y_Minus_Current. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_Y_Minus_Current = float4tohex(SP_Minus_CurrentMax + 1)

		try:
			SP_Z_VoltageInt = self.EPS.getSPZVoltage()
			SP_Z_Voltage = float4tohex(SP_Z_VoltageInt)
			if (SP_Z_VoltageInt < SP_VoltageMin) or (SP_Z_VoltageInt > SP_VoltageMax):
				print("SP_Z_VoltageInt: ", SP_Z_VoltageInt, "SP_Z_Voltage: ", SP_Z_Voltage)
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve SP_Z_Voltage. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_Z_Voltage = float4tohex(SP_VoltageMax + 1)

		try:
			SP_Z_Plus_CurrentInt = self.EPS.getSPZPlusCurrent()
			SP_Z_Plus_Current = float4tohex(SP_Z_Plus_CurrentInt)
			if (SP_Z_Plus_CurrentInt < SP_Plus_CurrentMin) or (SP_Z_Plus_CurrentInt > SP_Plus_CurrentMax):
				print("SP_Z_Plus_CurrentInt: ", SP_Z_Plus_CurrentInt, "SP_Z_Plus_Current: ", SP_Z_Plus_Current)
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve SP_Z_Current. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_Z_Plus_Current = float4tohex(SP_Plus_CurrentMax + 1)

			
		# print("packet type: " + packetType + "\ntimestamp: "+ timestamp + "\nmode: " + mode + 
		# "\nreboot count: " + reboot_count + "\nboombox uv: " + boombox_uv + 
		# "\nSPXPlusTemp " + SP_X_Plus_Temp + "\nSPZPlusTemp " + SP_Z_Plus_Temp + 
		# "\npitemp " + piTemp + "\nEPSMCUTemp " + EPSMCUTemp + "\nCell1Temp " + Cell1Temp + 
		# "\nCell2Temp " + Cell2Temp + "\nBattVoltage " + BattVoltage + "\nBattCurrent: " + BattCurrent + 
		# "\nBCRVoltage " + BCRVoltage + "\nBCRCurrent " + BCRCurrent + "\nE3V3Current " + EPS3V3Current + 
		# "\nEPS5VCurrent " + EPS5VCurrent + "\nSPXV " + SP_X_Voltage + "\nSPXPlusCurr " + SP_X_Plus_Current + 
		# "\nSPXMinusCurr " + SP_X_Minus_Current + "\nSPYV " + SP_Y_Voltage + "\nSPYPlusCurr " + SP_Y_Plus_Current + 
		# "\n SPYMinCurr " + SP_Y_Minus_Current + "\nSPZV " + SP_Z_Voltage + "\nSPZPlusCurr " + SP_Z_Plus_Current)

		packet += (gaspacsBytes + packetType + timestamp + mode + reboot_count + 
		boombox_uv + SP_X_Plus_Temp + SP_Z_Plus_Temp + piTemp + EPSMCUTemp + Cell1Temp + 
		Cell2Temp + BattVoltage + BattCurrent + BCRVoltage + BCRCurrent + EPS3V3Current + 
		EPS5VCurrent + SP_X_Voltage + SP_X_Plus_Current + SP_X_Minus_Current + SP_Y_Voltage + 
		SP_Y_Plus_Current + SP_Y_Minus_Current + SP_Z_Voltage + SP_Z_Plus_Current + gaspacsBytes)
		
		try:
			RTCInt = self.RTC.readSeconds()
			if (RTCInt< RTCMin) or (RTCInt > RTCMax):
				print("RTCInt: ", RTCInt)
				raise unexpectedValue
			packetTimestamp = str(RTCInt).zfill(10)+':'
		except Exception as e:
			print("Failed to pull from RTC. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
		self.__ttncData = packet

	async def writeData(self):
		#writes TTNC data array to file
		await self.__save.writeTTNC(self.__ttncData) 

	async def collectTTNCData(self, mMode):
		#we are going to wait 60 seconds after the pi boots before collecting data because the pi can be slow to update the system clock
		await asyncio.sleep(60)
		# Data collection loop
		while True:
			# Get TTNC data
			await self.getData(mMode)
			# Write data to file
			print("getting TTNC data")
			await self.writeData() # filechecker?
			# Sleep for 120 seconds (0.0083 Hz)
			await asyncio.sleep(120)

class DeployData():
	def __init__(self, saveobject):
		self.__save = saveobject
		self.RTC = Drivers.rtc.RTC()
		self.UVDriver = Drivers.UV.UVDriver() #may need to rework this if reduntant drivers are added
		self.__deployData = None
		self.Accelerometer = Drivers.Accelerometer()

	async def getData(self):
		#gets all Boom Deployment data
		packet = ''

		try:
			timestampInt = self.RTC.readMilliseconds()
			timestamp = int8tohex(timestampInt)
			if (timestampInt < RTCMinMil) or (timestampInt > RTCMaxMil):
				print("timestampInt: ", timestampInt, "timestamp: ", timestamp)
				raise unexpectedValue
		except Exception as e:
			print("Failed to pull clock data from RTC. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)

		packetType = int1tohex(2)

		try:
			boombox_uvFloat = self.UVDriver.read()
			boombox_uv = float4tohex(boombox_uvFloat)
			if (boombox_uvFloat < boombox_uvMin) or (boombox_uvFloat > boombox_uvMax):
				print("boombox_uvFloat: ", boombox_uvFloat, "boombox_uv: ", boombox_uv)
				raise unexpectedValue
		except Exception as e:
			# add redundant UVDriver try/except
			# if no UVDrivers work, continue with exception
			print("Failed to pull UVdriver data. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			boombox_uv = float4tohex(boombox_uvMax + 1)

		try:
			accelX, accelY, accelZ = self.Accelerometer.read()
			if ((accelX < accelMin) or (accelX > accelMax) or (accelY < accelMin) or (accelY > accelMax) or (accelZ < accelMin) or (accelZ > accelMax)):
				print("accelX: ", accelX, "accelY: ", accelY, "accelZ: ", accelZ)
				raise unexpectedValue
		except Exception as e:
			# add redundant UVDriver try/except
			# if no UVDrivers work, continue with exception
			print("Failed to pull Accelerometer. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			accelX, accelY, accelZ = accelMax + 1, accelMax + 1, accelMax + 1

		accelX = float4tohex(accelX)
		accelY = float4tohex(accelY)
		accelZ = float4tohex(accelZ)
		packet = ''
		packet += gaspacsBytes + packetType + timestamp + boombox_uv + accelX + accelY + accelZ + gaspacsBytes
		
		try:
			RTCInt = self.RTC.readSeconds()
			if (RTCInt < RTCMin) or (RTCInt > RTCMax):
				print("RTCInt: ", RTCInt)
				raise unexpectedValue
			packetTimestamp = str(RTCInt).zfill(10)+':'
		except Exception as e:
			# add redundant RTC try/except
			# if no RTC iterations work, continue with exception
			print("Failed to pull clock data from RTC. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)

		self.__deployData = packet
		print("Collected deploy data.")

	async def writeData(self):
		#writes Boom Deployment data array to file
		await self.__save.writeDeploy(self.__deployData) # filechecker?

	async def collectDeployData(self):
		# Data collection loop
		while True:
			#print("We are also stuck in this one")
			# Get Deploy data
			await self.getData()
			# Write data to file
			await self.writeData() # filechecker?
			#print("getting deployment data")
			# Sleep for 50 ms (20Hz)
			await asyncio.sleep(.005) #changing this will change the collection speed

class AttitudeData():
	def __init__(self, saveobject):
		self.save = saveobject
		self.RTC = Drivers.rtc.RTC() # may need rework with redundant drivers
		self.__attitudeData = None
		self.sunSensor = Drivers.sunSensors.sunSensorDriver.sunSensor()
		self.Magnetometer = Drivers.Magnetometer()
		self.__dataSamples = 1800
		self.__collectedData = 0

	async def getData(self):
		#gets all Attitude data
		packet = ''

		try:
			timestampInt = self.RTC.readSeconds()
			timestamp = int4tohex(timestampInt)
			if (timestampInt < RTCMin) or (timestampInt > RTCMax):
				print("timestampInt: ", timestampInt)
				raise unexpectedValue
		except Exception as e:
			# redundant RTC try/except
			# if no RTC works, continue with exception
			print("Failed to retrieve RTC data. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)

		packetType = int1tohex(0)

		try:
			allSunSensors = self.sunSensor.read() 
			sunSensor1, sunSensor2, sunSensor3, sunSensor4, sunSensor5 = [allSunSensors[i] for i in range(5)]

			if(sunSensor1 < sunSensorMin) or (sunSensor1 > sunSensorMax):
				print("sunSensor1: ", sunSensor1)
				raise unexpectedValue

			if(sunSensor2 < sunSensorMin) or (sunSensor2 > sunSensorMax):
				print("sunSensor2: ", sunSensor2)
				raise unexpectedValue

			if(sunSensor3 < sunSensorMin) or (sunSensor3 > sunSensorMax):
				print("sunSensor3: ", sunSensor3)
				raise unexpectedValue

			if(sunSensor4 < sunSensorMin) or (sunSensor4 > sunSensorMax):
				print("sunSensor4: ", sunSensor4)
				raise unexpectedValue

			if(sunSensor5 < sunSensorMin) or (sunSensor5 > sunSensorMax):
				print("sunSensor5: ", sunSensor5)
				raise unexpectedValue
		except Exception as e:
			# redundant sunSensor try/except, if none work, continue with exception
			print("Failed to pull data from sunSensor. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			sunSensor1 = sunSensorMax + 1
			sunSensor2 = sunSensorMax + 1
			sunSensor3 = sunSensorMax + 1
			sunSensor4 = sunSensorMax + 1
			sunSensor5 = sunSensorMax + 1

		sunSensor1 = float4tohex(sunSensor1)
		sunSensor2 = float4tohex(sunSensor2)
		sunSensor3 = float4tohex(sunSensor3)
		sunSensor4 = float4tohex(sunSensor4)
		sunSensor5 = float4tohex(sunSensor5)

		try:
			mag1, mag2, mag3 = self.Magnetometer.read()
			if ((mag1 < magnetometerMin) or (mag1 > magnetometerMax) or (mag2 < magnetometerMin) or (mag2 > magnetometerMax) or (mag3 < magnetometerMin) or (mag3 > magnetometerMax)):
				print("mag1: ", mag1, "mag2: ", mag2, "mag3: ", mag3)
				raise unexpectedValue
		except Exception as e:
			# redundant Magnetometers try/except
			mag1, mag2, mag3 = magnetometerMax + 1, magnetometerMax + 1, magnetometerMax + 1
			#print("Magnetometer values:", mag1, mag2, mag3, "Max and min", magnetometerMax, magnetometerMin)
			print("Failed to pull from Magnetometer. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			
		mag1 = float4tohex(mag1)
		mag2 = float4tohex(mag2)
		mag3 = float4tohex(mag3)

		packet += (gaspacsBytes + packetType + timestamp + sunSensor1 + 
		sunSensor2 + sunSensor3 + sunSensor4 + sunSensor5 + mag1 + mag2 + mag3 
		+ gaspacsBytes)
		
		#Print statement for debugging
		#print("timestamp: ", timestamp, "\npacketType: ", packetType, 
		# "\nsunSensor1: ", sunSensor1, "\nsunSensor2: ", sunSensor2, 
		# "\nsunSensor3: ", sunSensor3, "\nsunSensor4: ", sunSensor4, 
		# "\nsunSensor5 :", sunSensor5, "\nmag1: ", mag1, "\nmag2: ", mag2, 
		# "\nmag3: ", mag3)
		try:
			RTCInt = self.RTC.readSeconds()
			if (RTCInt < RTCMin) or (RTCInt > RTCMax):
				print("RTCInt: ", RTCInt)
				raise unexpectedValue
			packetTimestamp = str(RTCInt).zfill(10)+':'
		except Exception as e:
			# redundant rtc try/except
			print("Failed to pull clock data from RTC. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
		self.__attitudeData = packet
		print("Got attitude data.")

	async def writeData(self):
		#writes Attitude Data array to file
		await self.save.writeAttitude(self.__attitudeData) # filechecker?

	async def collectAttitudeData(self):
		#we are going to wait 60 seconds after the pi boots before collecting data because the pi can be slow to update the system clock
		await asyncio.sleep(60)
		
		# Data collection loop
		#this change will make it so that attitude data only collects 1800 times and then stops colleting 
		while self.__dataSamples >= self.__collectedData:
			# Get Attitude data
			await self.getData()
			# Write data to file
			await self.writeData()
			print("getting attitude data")
			# Sleep for 1 second (1 Hz)
			self.__collectedData += 1
			await asyncio.sleep(.9)#I dropped the wait time so that we will collect data more consitently 

def float4tohex(num):
	#takes a 4 byte float, returns a hex representation of it
	try:
		if(str(hex(struct.unpack('<I', struct.pack('<f', num))[0]))[2:] != '0'):
			return str(hex(struct.unpack('<I', struct.pack('<f', num))[0]))[2:]
		else:
			return str('00000000')
	except Exception as e:
		print("Failure to convert num in float4tohex. Exception: ", e, getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
		return str('00000000')

def int4tohex(num):
	#takes a 4 byte int, returns a hex representation of it
	try:
		return str(format(num, '08x'))[-8:]
	except Exception as e:
		print("Failure to convert num in int4tohex. Exception: ", e, getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
		return str(format(0, '08x'))[-8:]

def int1tohex(num):
	#takes a 1 byte integer, returns a hex representation of it
	try:
		return str(format(num, '02x'))[-2:]
	except Exception as e:
		print("Failure to convert num in int1tohex Exception: ", e, getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
		return str(format(0, '02x'))[-2:]

def int2tohex(num):
	#takes a 2 byte integer, returns a hex representation of it
	try:
		return str(format(num, '04x'))[-4:]
	except Exception as e:
		print("Failure to convert num in int2tohex. Exception: ", e, getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
		return str(format(0, '04x'))[-4:]

def int8tohex(num):
	#takes an 8 byte integer, returns a hex representation of it
	try:
		return str(format(num, '016x'))[-16:]
	except Exception as e:
		print("Failure to convert num in int8tohex. Exception: ", e, getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
		return str(format(0, '016x'))[-16:]

class unexpectedValue(Exception):
	print("Received unexpected value.", getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
	pass
