import sys
sys.path.append('../')
from Drivers.eps import EPS
from time import sleep

epsTest = EPS()

#Test battery raw disable/enable
epsTest.enableRaw()
print("Raw Battery Voltage Enabled for 10 seconds")
sleep(10)
epsTest.disableRaw()
print("Raw Battery Voltage Disabled for 10 seconds")
sleep(10)
epsTest.enableRaw()
print("Raw Battery Voltage Re-enabled")

#Test all read functions
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
print("Tests done. Exiting.")
