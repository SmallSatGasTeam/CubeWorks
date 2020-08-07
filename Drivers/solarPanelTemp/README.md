Solar Panel Temperature Driver:
--
Location: ../Drivers/solarPanelTemp/solarDriver.py

Functionality:
	The Solar Panel Temperature Driver establishes an SPi connection through the ADC to the two Temperature Sensors connected to the solar panels. After the connection is established this driver can return the temperature of the solar panels. In order to gain access to this data call: solarDriver.TempSensor.read().
	