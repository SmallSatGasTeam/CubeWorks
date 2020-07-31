Watchdog:
--
Location: ../watchdog/ardunioTapB1_v4_I2C/ardunioTapB1_v4_I2C.ino
	
Functionality:
	The Watchdog lives in the Arduino Beetle. This code makes sure that the Raspberry Pi stays alive. It is the Raspberry Pi’s guardian. It manages when the Raspberry Pi turns on or off. Whenever the satellite goes into SAFE (see GASPACS Flight Logic Plan Outline) the watchdog will turn the Pi off till it is safe for it to turn back on. The Watchdog will also listen to the ‘Heartbeat’ of the Raspberry Pi to make sure that it is running as it should and did not die. If there is a silence that lasts over four seconds from the Raspberry Pi then the Watchdog reboots it.
