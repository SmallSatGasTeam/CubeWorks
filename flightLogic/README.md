GASPACS Software: The Flight Software
==
Opening Note:
	 The Flight Logic Plan Outline document goes into greater details on the individual mission modes. This document will explain things more simply. Please read Flight Logic Plan Outline.

Flight Logic/the Main File:
--
Location: ../flightLogic/flightLogic.py

Functionality:
		This file will manage all our mission modes outlines in the Flight Logic Plan Outline. All these modes will be run in other files except for the BOOT mission mode. This will be run inside the file flightLogic.py. This file will run all the other mission modes and make sure we are going through them in the right order and completing them successfully. This file also gets Attitude, Boom Deployment and TTNC data gathered by the getDriverData.py file.

Getting the Data From the Drivers:
--
Location: ../flightLogic/flightLogic.py

Functionality:
		This file calls on the drivers to gather and organize the TTNC, Boom Deployment and Attitude data. This data is then used in the flightLogic.py file to determine if we are able to execute certain modes.

Boot Records and Backup Boot Records:
--
Location: ../flightLogic/bootRecords 
	    ../flightLogic/backupBootRecords

Purpose:
	These are simple text files. They will store in the first line how many times we have booted, in the second line whether we are on the first boot, in the third line whether the antenna have been deployed and in the fourth line what our last mission mode was. We have multiple files with this same data to prevent losing the data.

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
--
Location: ../flightLogic/missionModes/boomDeploy.py

Functionality:
		The Boom Deployment Mode will run after all the checks performed by the Pre-Boom Deployment mode. The Boom Deployment mode will run the Boom Deployer Driver and then the Camera Driver. (see GASPACA Software I: the Drivers)

Post-Boom Deploy mode:
--
Location: ../flightLogic/missionModes/postBoomDeploy.py

Functionality:
		This is the last mission mode the Raspberry Pi enters. Once all modes have been run this mode will run a Reboot loop. This loop will cause a reboot every twenty-four hours. This mode will monitor the battery power and other basic functions to keep our satellite from dying. This is also the mode that transmission will take place in. 


SAFE:
--
Location: ../flightLogic/missionModes/safe.py

Functionality:
	This mode will turn the Raspberry Pi off. It does this by sending a signal to the Arduino Beetle to turn it off. This is to protect against damage to the Pi and lose of data.


