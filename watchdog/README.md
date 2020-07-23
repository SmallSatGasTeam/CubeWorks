GASPACS Software II: The Watchdog Protocol 
==
Watchdog:
--
Location: ../watchdog/ardunioTapB1_v4_I2C/ardunioTapB1_v4_I2C.ino
	
Functionality:
	The Watchdog lives in the Arduino Beetle. This code makes sure that the Raspberry Pi stays alive. It is the Raspberry Pi’s guardian. It manages when the Raspberry Pi turns on or off. Whenever the satellite goes into SAFE (see GASPACS Flight Logic Plan Outline) the watchdog will turn the Pi off till it is safe for it to turn back on. The Watchdog will also listen to the ‘Heartbeat’ of the Raspberry Pi to make sure that it is running as it should and did not die. If there is a silence that lasts over four seconds from the Raspberry Pi then the Watchdog reboots it.


Heartbeat:
--
Location: ../watchdog/Heartbeat/Heartbeat.py

Functionality:
	The code in Heartbeat.py is the ‘Heartbeat’ of the Raspberry Pi. It sends a five macro-second pulse every four seconds over a pin that connects theRaspberry Pi to the Arduino Beetle where the Watchdog ‘listens’ for the pulse. 


