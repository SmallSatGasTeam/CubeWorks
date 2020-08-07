Magnetometer Driver:
--
Location: ../Drivers/Magnetometer/Magnetometer.py

Functionality:
	The Magnetometer Driver establishes an I2C connection with the Magnetometer. Once that connection is made the driver will then collect information concerning the direction, strength, or relative change of magnetic fields in relation to the satellite that have been gathered by the Magnetometer. To gain access to this information call Magnetometer.Magnetometer.read()
