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
EPS5VCurrentMax = 2.0
sunSensorMin = 0.0
sunSensorMax = 3.3
RTCMin = 0
RTCMax = 4294967295
RTCMinMil = 0
RTCMaxMil = 4294967295 * 1000
magnetometerMin = -49.151
magnetometerMax = 49.152

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
		
		packetType = int1tohex(1)
		mode = int1tohex(missionMode)
		reboot_count = int2tohex(readBootCount())
		#No need for await on these, since they're not sleeping
		try:
			boombox_uv = float4tohex(self.UVDriver.read()) 
			if (boombox_uv < float4tohex(boombox_uvMin)) or (boombox_uv > float4tohex(boombox_uvMax)):
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
			piTemp = float4tohex(self.CpuTempSensor.read())
			if (piTemp < float4tohex(piTempMin)) or (piTemp > float4tohex(piTempMax)):
				raise unexpectedValue
		except Exception as e:
			# add redundant CpuTempSensor TRY/EXCEPT
			# if no drivers can be called, continue with exception
			print("Failed to retrieve cpuTempSensor. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			piTemp = float4tohex(piTempMax + 1)

		try:
			EPSMCUTemp = float4tohex(self.EPS.getMCUTemp())
			if ((EPSMCUTemp < float4tohex(EPSMCUMin)) or (EPSMCUTemp > float4tohex(EPSMCUMax))):
				print("unexpected value eps mcu temp")
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve EPSMCUTemp. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			EPSMCUTemp = float4tohex(EPSMCUMax + 1)

		try:
			Cell1Temp = float4tohex(self.EPS.getCell1Temp())
			if ((Cell1Temp < float4tohex(Cell1TempMin)) or (Cell1Temp > float4tohex(Cell1TempMax))):
				print("Unexpected value recieved from cell temp 1")
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve Cell1Temp. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			Cell1Temp = float4tohex(Cell1TempMax + 1)

		try:
			Cell2Temp = float4tohex(self.EPS.getCell2Temp())
			if ((Cell2Temp < float4tohex(Cell2TempMin)) or (Cell2Temp > float4tohex(Cell2TempMax))):
				print("unexpected value recieved from cell temp 2")
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve Cell2Temp. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			Cell2Temp = float4tohex(Cell2TempMax + 1)

		try:
			print("BattVoltage: ", self.EPS.getBusVoltage())
			BattVoltage = float4tohex(self.EPS.getBusVoltage())
			if ((BattVoltage < float4tohex(BattVoltageMin)) or (BattVoltage > float4tohex(BattVoltageMax))):
				raise unexpectedValue
		except Exception as e:
			BattVoltage = float4tohex(BattVoltageMax + 1)
			print("failed to retrieve BattVoltage. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno,
			"Received: ", BattVoltage)

		try:
			BattCurrent = float4tohex(self.EPS.getBusCurrent())
			if (BattCurrent < float4tohex(BattCurrentMin)) or (BattCurrent > float4tohex(BattCurrentMax)):
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve BattCurrent. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			BattCurrent = float4tohex(BattCurrentMax + 1)

		try:
			print("getDriverData: ", self.EPS.getBCRVoltage())
			BCRVoltage = float4tohex(self.EPS.getBCRVoltage())
			if ((BCRVoltage < float4tohex(BCRVoltageMin)) or (BCRVoltage > float4tohex(BCRVoltageMax))):
				raise unexpectedValue
		except Exception as e:
			BCRVoltage = float4tohex(BCRVoltageMax + 1)
			print("failed to retrieve BCRVoltage. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno, 
			"Received: ", BCRVoltage)

		try:
			BCRCurrent = float4tohex(self.EPS.getBCRCurrent())
			if (BCRCurrent < float4tohex(BCRCurrentMin)) or (BCRCurrent > float4tohex(BCRCurrentMax)):
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve BCRCurrent. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			BCRCurrent = float4tohex(BCRCurrentMax + 1)

		try:
			EPS3V3Current = float4tohex(self.EPS.get3V3Current())
			if (EPS3V3Current < float4tohex(EPS3V3CurrentMin)) or (EPS3V3Current > float4tohex(EPS3V3CurrentMax)):
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve EPS3V3Current. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			EPS3V3Current = float4tohex(EPS3V3CurrentMax + 1)

		try:
			EPS5VCurrent = float4tohex(self.EPS.get5VCurrent())
			if (EPS5VCurrent < float4tohex(EPS5VCurrentMin)) or (EPS5VCurrent > float4tohex(EPS5VCurrentMax)):
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve EPS5VCurrent. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			EPS5VCurrent = float4tohex(EPS5VCurrentMax + 1)

		try:
			SP_X_Voltage = float4tohex(self.EPS.getSPXVoltage())
			if (SP_X_Voltage < float4tohex(SP_VoltageMin)) or (SP_X_Voltage > float4tohex(SP_VoltageMax)):
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve SP_X_Voltage. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_X_Voltage = float4tohex(SP_VoltageMax + 1)

		try:
			SP_X_Plus_Current = float4tohex(self.EPS.getSPXPlusCurrent())
			if (SP_X_Plus_Current < float4tohex(SP_Plus_CurrentMin)) or (SP_X_Plus_Current > float4tohex(SP_Plus_CurrentMax)):
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve SP_X_Plus_Current. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_X_Plus_Current = float4tohex(SP_Plus_CurrentMax + 1)

		try:
			SP_X_Minus_Current = float4tohex(self.EPS.getSPXMinusCurrent())
			if (SP_X_Minus_Current < float4tohex(SP_Minus_CurrentMin)) or (SP_X_Minus_Current > float4tohex(SP_Minus_CurrentMax)):
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve SP_X_Minus_Current. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_X_Minus_Current = float4tohex(SP_Minus_CurrentMax + 1)

		try:
			SP_Y_Voltage = float4tohex(self.EPS.getSPYVoltage())
			if (SP_Y_Voltage < float4tohex(SP_VoltageMin)) or (SP_Y_Voltage > float4tohex(SP_VoltageMax)):
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve SP_Y_Voltage. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_Y_Voltage = float4tohex(SP_VoltageMax + 1)

		try:
			SP_Y_Plus_Current = float4tohex(self.EPS.getSPYPlusCurrent())
			if (SP_Y_Plus_Current < float4tohex(SP_Plus_CurrentMin)) or (SP_Y_Plus_Current > float4tohex(SP_Plus_CurrentMax)):
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve SP_Y_Plus_Current. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_Y_Plus_Current = float4tohex(SP_Plus_CurrentMax + 1)

		try:
			SP_Y_Minus_Current = float4tohex(self.EPS.getSPYMinusCurrent())
			if(SP_Y_Minus_Current < float4tohex(SP_Minus_CurrentMin)) or (SP_Y_Minus_Current > float4tohex(SP_Minus_CurrentMax)):
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve SP_Y_Minus_Current. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_Y_Minus_Current = float4tohex(SP_Minus_CurrentMax + 1)

		try:
			SP_Z_Voltage = float4tohex(self.EPS.getSPZVoltage())
			if (SP_Z_Voltage < float4tohex(SP_VoltageMin)) or (SP_Z_Voltage > float4tohex(SP_VoltageMax)):
				raise unexpectedValue
		except Exception as e:
			print("failed to retrieve SP_Z_Voltage. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			SP_Z_Voltage = float4tohex(SP_VoltageMax + 1)

		try:
			SP_Z_Plus_Current = float4tohex(self.EPS.getSPZPlusCurrent())
			if (SP_Z_Plus_Current < float4tohex(SP_Plus_CurrentMin)) or (SP_Z_Plus_Current > float4tohex(SP_Plus_CurrentMax)):
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
			if (self.RTC.readSeconds() < RTCMin) or (self.RTC.readSeconds() > RTCMax):
				raise unexpectedValue
			packetTimestamp = str(int(self.RTC.readSeconds())).zfill(10)+':'
		except Exception as e:
			print("Failed to pull from RTC. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)

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
			timestamp = int8tohex(self.RTC.readMilliseconds())
			if (timestamp < int8tohex(RTCMinMil)) or (timestamp > int8tohex(RTCMaxMil)):
				raise unexpectedValue
		except Exception as e:
			print("Failed to pull clock data from RTC. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)

		packetType = int1tohex(2)

		try:
			boombox_uv = float4tohex(self.UVDriver.read())
			if (boombox_uv < float4tohex(boombox_uvMin)) or (boombox_uv > float4tohex(boombox_uvMax)):
				raise unexpectedValue
		except Exception as e:
			# add redundant UVDriver try/except
			# if no UVDrivers work, continue with exception
			# print("Failed to pull UVdriver data. Exception: ", repr(e), 
			# getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			boombox_uv = float4tohex(boombox_uvMax + 1)

		try:
			accelX, accelY, accelZ = self.Accelerometer.read()
			if ((accelX < accelMin) or (accelX > accelMax) or (accelY < accelMin) or (accelY > accelMax) or (accelZ < accelMin) or (accelZ > accelMax)):
				raise unexpectedValue
		except Exception as e:
			# add redundant UVDriver try/except
			# if no UVDrivers work, continue with exception
			# print("Failed to pull Accelerometer. Exception: ", repr(e), 
			# getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
			accelX, accelY, accelZ = accelMax + 1, accelMax + 1, accelMax + 1

		accelX = float4tohex(accelX)
		accelY = float4tohex(accelY)
		accelZ = float4tohex(accelZ)
		packet = ''
		packet += gaspacsBytes + packetType + timestamp + boombox_uv + accelX + accelY + accelZ + gaspacsBytes
		
		try:
			if (self.RTC.readSeconds() < RTCMin) or (self.RTC.readSeconds() > RTCMax):
				raise unexpectedValue
			packetTimestamp = str(int(self.RTC.readSeconds())).zfill(10)+':'
		except Exception as e:
			# add redundant RTC try/except
			# if no RTC iterations work, continue with exception
			print("Failed to pull clock data from RTC. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)

		packet = packetTimestamp + packet
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

	async def getData(self):
		#gets all Attitude data
		packet = ''

		try:
			timestamp = int4tohex(self.RTC.readSeconds())
			if (self.RTC.readSeconds() < RTCMin) or (self.RTC.readSeconds() > RTCMax):
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
				raise unexpectedValue

			if(sunSensor2 < sunSensorMin) or (sunSensor2 > sunSensorMax):
				raise unexpectedValue

			if(sunSensor3 < sunSensorMin) or (sunSensor3 > sunSensorMax):
				raise unexpectedValue

			if(sunSensor4 < sunSensorMin) or (sunSensor4 > sunSensorMax):
				raise unexpectedValue

			if(sunSensor5 < sunSensorMin) or (sunSensor5 > sunSensorMax):
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
			if (self.RTC.readSeconds() < RTCMin) or (self.RTC.readSeconds() > RTCMax):
				raise unexpectedValue
			packetTimestamp = str(int(self.RTC.readSeconds())).zfill(10)+':'
		except Exception as e:
			# redundant rtc try/except
			print("Failed to pull clock data from RTC. Exception: ", repr(e), 
			getframeinfo(currentframe()).filename, getframeinfo(currentframe()).lineno)
		
		packet = packetTimestamp + packet
		self.__attitudeData = packet
		print("Got attitude data.")

	async def writeData(self):
		#writes Attitude Data array to file
		await self.save.writeAttitude(self.__attitudeData) # filechecker?

	async def collectAttitudeData(self):
		# Data collection loop
		while True:
			# Get Attitude data
			await self.getData()
			# Write data to file
			await self.writeData()
			print("getting attitude data")
			# Sleep for 1 second (1 Hz)
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