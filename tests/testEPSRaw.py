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
print("Raw Battery Voltage Re-enabled for 10 seconds")
sleep(10)
epsTest.disableRaw()
print("Raw Battery Voltage Disabled. Test complete")
