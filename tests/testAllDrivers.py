# This file will test all of the GASPACS Sensor Drivers. A successful test will result in a valid output for each Driver.
# Note, the following drivers are not tested because they're not sensors: Backup Antenna Deployer, Boom Deployer, EPS Raw, Heartbeat, Interrupt, SolarPower, TransceiverConfig, Watchdog Commands

# Append ../ directory to path so Drivers can be found
import sys
sys.path.append("../")

# Imports
import numpy as np
from Drivers.adc import ADC_Driver
from Drivers import Accelerometer
from Drivers.antennaDoor import AntennaDoor
from Drivers.camera import Camera
from Drivers.cpuTemperature import CpuTemperature
from Drivers.eps import EPS
from Drivers.Magnetometer import Magnetometer
from Drivers.rtc import RTC
from Drivers.solarPanelTemp import solarDriver
from Drivers.sunSensors import sunSensorDriver
from Drivers.UV import UVDriver

# Test ADC Driver
adc = ADC_Driver.ADC()
for i in range(0,6):
    print("ADC Readings: ", adc.read(i))

# Test Accelerometer Driver
accel = Accelerometer()
print("Accelerometer: ", accel.read())
print("Accelerometer Magnitude: ", np.linalg.norm(accel.read()))

# Antenna Door Driver
antennaDoor = AntennaDoor()
print("Antenna Door: ", antennaDoor.readDoorStatus())

# Camera Driver
# Take Picture
cameraObject = Camera()
pictureNumber = cameraObject.takePicture()
print("Picture Number: ", pictureNumber)

# Compress Low Res and High Res To Files
cameraObject.compressLowResToFiles(pictureNumber)
print("Low Res Pic Compressed")
cameraObject.compressHighResToFiles(pictureNumber)
print("High Res Pic Compressed")

# CPU Temperature Driver
cpu = CpuTemperature()
print("CPU Temp: ", cpu.read())

# Test EPS Read
epsTest = EPS()
print("MCU Temp in C: "+str(epsTest.getMCUTemp()))
print("Cell 1 Temp in C: "+str(epsTest.getCell1Temp()))
print("Cell 2 Temp in C: "+str(epsTest.getCell2Temp()))
print("Bus Voltage in V: "+str(epsTest.getBusVoltage()))
print("Bus Current in A: "+str(epsTest.getBusCurrent()))
print("Battery Charge Regulator Voltage in V: "+str(epsTest.getBCRVoltage()))
print("Battery Charge Regulator Current in A: "+str(epsTest.getBCRCurrent()))
print("3V3 Current in A: "+str(epsTest.get3V3Current()))
print("5V Current in A: "+str(epsTest.get5VCurrent()))
print("X-Axis Solar Panel Voltage in V: "+str(epsTest.getSPXVoltage()))
print("X- Solar Panel Current in A: "+str(epsTest.getSPXMinusCurrent()))
print("X+ Solar Panel Current in A: "+str(epsTest.getSPXPlusCurrent()))
print("Y-Axis Solar Panel Voltage in V: "+str(epsTest.getSPYVoltage()))
print("Y- Solar Panel Current in A: "+str(epsTest.getSPYMinusCurrent()))
print("Y+ Solar Panel Current in A: "+str(epsTest.getSPYPlusCurrent()))
print("Z-Axis Solar Panel Voltage in V: "+str(epsTest.getSPZVoltage()))
print("Z+ Solar Panel Current in A: "+str(epsTest.getSPZPlusCurrent()))

# Test Magnetometer
mag = Magnetometer()
print("Magnetometer: ", mag.read())
print("Magnetometer Magnitude: ", np.linalg.norm(mag.read()))

# RTC Driver
rtc = RTC()
print("RTC Milliseconds: ", rtc.readMilliseconds())
print("RTC Seconds: ", rtc.readSeconds())

# Solar Panel Temp Driver
tempSensors = solarDriver.TempSensor()
print("Solar Panel Temp Sensors: ", tempSensors.read())

# Sun Sensors Driver
sun = sunSensorDriver.sunSensor()
print("Sun Sensors: ", sun.read())

# UV Sensor Driver
uv = UVDriver()
print("UV Sensor: ", uv.read())
