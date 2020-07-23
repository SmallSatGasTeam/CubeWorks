GASPACS Software VI: The Flight Software
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
