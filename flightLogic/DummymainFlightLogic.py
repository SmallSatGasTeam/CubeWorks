# This is the main file, to be run on startup of the Pi
import sys
sys.path.append('../')
import os.path
from flightLogic import DummygetDriverData as getDriverData
import flightLogic.saveTofiles as saveTofiles
from DummyDrivers.antennaDoor.AntennaDoor import AntennaDoor as antennaDoor
from flightLogic.DummymissionModes.antennaDeploy import antennaMode as antennaMode
from flightLogic.DummymissionModes.preBoomDeploy import preBoomMode
from flightLogic.DummymissionModes.boomDeploy import boomMode
from flightLogic.DummymissionModes.postBoomDeploy import postBoomMode
from flightLogic.DummymissionModes import safe
from protectionProticol.fileProtection import FileReset as fileChecker
import asyncio
from TXISR import pythonInterrupt


# from TXISR import interrupt
# NOTE: The TXISR needs to run as a separate thread, and is not asyncio
# import thread @@Shawn This import isn't working

# executeFlightLogic()
"""
 First, this function sets up the TXISR and then checks the boot conditions
 Then, it runs a mission mode, and then loops forever, constantly checking to run the next mission mode.
 NOTE: Each mission mode evaluates their exit conditions to leave the mission mode.
 NOTE: Each mission mode calls safe if it is necessary
 NOTE: DO NOTE record safe mode in the bootRecords file

"""

def __main__():
	asyncio.run(executeFlightLogic())

fileCheck = fileChecker()
#hey

async def executeFlightLogic():  # Open the file save object, start TXISR, and start Boot Mode data collection
	# Variable setup
	delay = 1*60  # 35 minute delay
	boot = True
	save = saveTofiles.save()
	# startTXISR(save)
	ttncData = getDriverData.TTNCData(save)
	attitudeData = getDriverData.AttitudeData(save)
	safeMode = safe.safe(save)
	#interruptObject = INTERRUPT()

	print('Starting data collection') #Setting up Background tasks for BOOT mode
	tasks=[]
	tasks.append(asyncio.create_task(pythonInterrupt.interrupt()))
	tasks.append(asyncio.create_task(ttncData.collectTTNCData(0))) #Boot Mode is classified as 0
	tasks.append(asyncio.create_task(attitudeData.collectAttitudeData()))
	tasks.append(asyncio.create_task(safeMode.thresholdCheck()))
	tasks.append(asyncio.create_task(safeMode.heartBeat()))

	# Initialize all mission mode objects
	# NOTE: the comms-tx is the only exception to this rule as it is to be handled differently than other mission modes
	# NOTE: Boot Mode is defined and executed in this document, instead of a separate mission mode
	antennaDeploy = antennaMode(save)
	preBoomDeploy = preBoomMode(save)
	postBoomDeploy = postBoomMode(save)
	boomDeploy = boomMode(save)

	if(readData() == (None, None, None)):
		print('Files are empty')
		bootCount, antennaDeployed, lastMode = 0,False,0
	else:
		bootCount, antennaDeployed, lastMode = readData()  # Read in data from files
	bootCount += 1  # Increment boot count
	recordData(bootCount, antennaDeployed, lastMode)

	if lastMode not in range(0,7): #Mission Mode invalid
		lastMode = 0
		antennaDeployed = False

	# This is the implementation of the BOOT mode logic.
	if not antennaDeployed:  # First, sleep for 35 minutes
		print('Antenna is undeployed, waiting 35 minutes')
		await asyncio.sleep(delay)  # Sleep for 35 minutes

	try:  # Cancels attitude collection tasks
		for t in tasks:
			t.cancel()
		print('Successfully cancelled BOOT mode background tasks')
	except asyncio.exceptions.CancelledError:
		print("Exception thrown cancelling task - This is normal")

	# how do we check if the antenna doors are open?
	# TODO, check of antenna doors are open
	print('Moving on to check antenna door status')
	status = antennaDoor().readDoorStatus()
	# this checks the bytes returned by the antennaDoor if any are 0 then doorOpen gets set to false
	if antennaDeployed == True:
		pass
	elif status == (1,1,1,1): #This will need to be changed to reflect the real antenna
		antennaDeployed = True
	else:
        antennaDeployed = False

	recordData(bootCount, antennaDeployed, lastMode)

	if not antennaDeployed:
		print('Running Antenna Deployment Mode')
		await asyncio.gather(antennaDeploy.run())
		antennaDeployed = True
		print(antennaDeployed)
		recordData(bootCount, antennaDeployed, lastMode)  # Save into files
	elif lastMode == 4:
		print('Running Post Boom Deploy')
		lastMode = 4
		await asyncio.gather(postBoomDeploy.run())
	else:
		print('Running preBoom Deploy')
		lastMode = 2
		await asyncio.gather(preBoomDeploy.run())


	while True: # This loop executes the rest of the flight logic
	# pre boom deploy
		if antennaDeployed == True and lastMode not in (3,4):
			print('Running pre-Boom deploy')
			lastMode = 2
			recordData(bootCount, antennaDeployed, lastMode)
			await asyncio.gather(preBoomDeploy.run())  # Execute pre-boom deploy, then move to post-boom deploy
			lastMode = 3
			recordData(bootCount, antennaDeployed, lastMode)
		elif antennaDeployed == True and lastMode == 3:
			print('Running Boom Deploy')
			await asyncio.gather(boomDeploy.run())  # Execute boom deployment, start post-boom deploy
			lastMode = 4
			recordData(bootCount, antennaDeployed, lastMode)
		else:  # Post-Boom Deploy
			print('Running post-Boom Deploy')
			await asyncio.gather(postBoomDeploy.run())


def recordData(bootCount, antennaDeployed, lastMode):
	fileCheck.checkFile("/home/pi/testingStartup/flightLogicData/bootRecords.txt")
	# write to the boot file, "w" option in write overwrites the file
	new = open("/home/pi/testingStartup/flightLogicData/bootRecords.txt", "w+")
	new.write(str(bootCount) + '\n')
	if antennaDeployed:
		new.write(str(1)+'\n')
	else:
		new.write(str(0)+'\n')
	new.write(str(lastMode) + '\n')
	new.close()

	# write to the the back up file
	fileCheck.checkFile("/home/pi/testingStartup/flightLogicData/backupBootRecords.txt")
	new = open("/home/pi/testingStartup/flightLogicData/backupBootRecords.txt", "w+")
	new.write(str(bootCount) + '\n')
	if antennaDeployed:
		new.write(str(1)+'\n')
	else:
		new.write(str(0)+'\n')
	new.write(str(lastMode) + '\n')
	new.close()


def readData():
	# This function reads in data from the files, it was previously in the main function but is better as its own function
	# bootRecords file format
	# Line 1 = boot count
	# Line 2 = antenna deployed?
	# Line 2 = last mission mode
	bootCount,antennaDeployed,lastMode = None, None, None
	fileCheck.checkFile("/home/pi/testingStartup/flightLogicData/bootRecords.txt")
	try:
		bootFile = open("/home/pi/testingStartup/flightLogicData/bootRecords.txt", "r")
		bootCount = int(bootFile.readline().rstrip())
		antennaDeployed = bool(int(bootFile.readline().rstrip()))
		lastMode = int(bootFile.readline().rstrip())
		bootFile.close()
	except:
		try:
			print('File exception')
			fileCheck.checkFile("/home/pi/testingStartup/flightLogicData/backupBootRecords.txt")
			bootFile = open("/home/pi/testingStartup/flightLogicData/backupBootRecords.txt", "r")
			bootCount = int(bootFile.readline().rstrip())
			antennaDeployed = bool(int(bootFile.readline().rstrip()))
			lastMode = int(bootFile.readline().rstrip())
			bootFile.close()
			# In this except statement, the files are corrupted, so we rewrite both of them
		except:
			print('Double File exception - are both files non-existant?')
			fileCheck.checkFile("/home/pi/testingStartup/flightLogicData/bootRecords.txt")
			bootFile = open("/home/pi/testingStartup/flightLogicData/bootRecords.txt", "w")
			fileCheck.checkFile("/home/pi/testingStartup/flightLogicData/backupBootRecords.txt")
			backupBootFile = open("/home/pi/testingStartup/flightLogicData/backupBootRecords.txt", "w")
			bootFile.write('0\n0\n0\n')
			backupBootFile.write('0\n0\n0\n')

	recordData(bootCount, antennaDeployed, lastMode)
	return bootCount, antennaDeployed, lastMode


# def startTXISR(saveobject):  # Setup for TXISR
# This sets up the interupt on the uart pin that triggers when we get commincation over uart
# thread.start(interrupt.watchReceptions(saveobject)) <-- TODO fix that import