import sys
sys.path.append("../")

from Drivers.sunSensors import sunSensorDriver

sun = sunSensorDriver.sunSensor()
print(sun.read())
