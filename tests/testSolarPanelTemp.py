import sys
sys.path.append("../")

from Drivers.solarPanelTemp import solarDriver


tempSensors = solarDriver.TempSensor()
print(tempSensors.read())
