Mission Modes
==
Antenna Deploy Mode:
--
Location: ../flightLogic/missionModes/antennaDeploy.py

Functionality: 
		In the file flightLogic.py there is a section of code that will check if the antennas have been deployed using our antenna door driver (see GASPACS Software I: the Drivers).  If this check returns false the antenna deploy mode will run. This mode will check our battery to see if we have enough power to open the doors. If that check returns true we will then call our back up antenna deployment driver (see GASPACA Software I: the Drivers). If we do not have enough power we will go into sage mode. 

Pre Boom Deployment mode:
--
Location: ../flightLogic/missionModes/preBoomDeploy.py

Functionality:
		When we go into Pre Boom Deployment mode we perform multiple checks. These checks are to insure the satellite is exposed to the sun where our Aero Boom can cure and stiffen as well as to make sure we have enough power. To get the data needed (TTNC, Attitude and Boom Deployment data) to perform these checks the Pre Boom Deployment Mode code will call the getDriverData class.

Boom Deployment mode:
---
Location: ../flightLogic/missionModes/boomDeploy.py

Functionality:
		The Boom Deployment Mode will run after all the checks performed by the Pre-Boom Deployment mode. The Boom Deployment mode will run the Boom Deployer Driver and then the Camera Driver. (see GASPACA Software I: the Drivers)

Post-Boom Deploy mode:
---
Location: ../flightLogic/missionModes/postBoomDeploy.py

Functionality:
		This is the last mission mode the Raspberry Pi enters. Once all modes have been run this mode will run a Reboot loop. This loop will cause a reboot every twenty-four hours. This mode will monitor the battery power and other basic functions to keep our satellite from dying. This is also the mode that transmission will take place in. 
Heartbeat:
---

Functionality:
	The code in Heartbeat.py is the ‘Heartbeat’ of the Raspberry Pi. It sends a five macro-second pulse every four seconds over a pin that connects theRaspberry Pi to the Arduino Beetle where the Watchdog ‘listens’ for the pulse. 

Transmitting:
---
	This code handles watching the tx windows, preparing the data 20 seconds before it is time to transmit, and calling the transmission runtine when it is time to transmit.