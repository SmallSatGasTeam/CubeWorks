import sys
sys.path.append('../')
from Drivers.eps import EPS
from time import sleep

epsTest = EPS()

#Test solar panel charge functions
print("Bus Voltage in V: "+str(epsTest.getBusVoltage()))
print("Bus Current in A: "+str(epsTest.getBusCurrent()))
print("Battery Charge Regulator Voltage in V: "+str(epsTest.getBCRVoltage()))
print("Battery Charge Regulator Current in A: "+str(epsTest.getBCRCurrent()))
print("X-Axis Solar Panel Voltage in V: "+str(epsTest.getSPXVoltage()))
print("X+ Solar Panel Current in A: "+str(epsTest.getSPXPlusCurrent()))
