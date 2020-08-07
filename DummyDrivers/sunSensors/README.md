Sun Sensor Driver:
--
Location: ../Drivers/sunSensors/sunSensorDriver.py

Functionality:
	The Sun Sensor Driver uses the ADC Drivers already established SPi connection. (See ADC Driver) Using polymorphism this driver reads in from multiple channels of communication via the ADC’s read() function. These channels are connected to the five Sun Sensors. The data collected from these sensors can be accessed by calling: sunSensorDriver.SunSensor.read() 
