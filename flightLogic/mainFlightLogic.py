# This is the main file, to be run on startup of the Pi
import sys
sys.path.append('../')
import os.path
from flightLogic import getDriverData
import flightLogic.saveTofiles as saveTofiles
from Drivers.antennaDoor.AntennaDoor import AntennaDoor as antennaDoor
from flightLogic.missionModes.antennaDeploy import antennaMode as antennaMode
from flightLogic.missionModes.preBoomDeploy import preBoomMode
from flightLogic.missionModes.boomDeploy import boomMode
from flightLogic.missionModes.postBoomDeploy import postBoomMode
from flightLogic.missionModes.heartBeat import heart_beat
# from flightLogic.missionModes import safe
from flightLogic.missionModes.transmitting import Transmitting
from flightLogic.missionModes import *
from protectionProticol.fileProtection import FileReset
import asyncio
from TXISR import pythonInterrupt
from TXISR.packetProcessing import packetProcessing
from Drivers.camera import Camera
from Drivers.eps import EPS as EPS




# from TXISR import interrupt
# NOTE: This Code has past unit testing

##################################################################################################################
# executeFlightLogic()
##################################################################################################################
# First, this function sets up the TXISR and then checks the boot conditions
# Then, it runs a mission mode, and then loops forever, constantly checking to run the next mission mode.
# NOTE: Each mission mode evaluates their exit conditions to leave the mission mode.
##################################################################################################################
fileChecker = FileReset()

def __main__():
	asyncio.run(executeFlightLogic())


async def executeFlightLogic():  # Open the file save object, start TXISR, camera obj, and start Boot Mode data collection
	
	baseFile = open("/home/pi/lastBase.txt")
	codeBase = int(baseFile.read())
	cameraObj = Camera()
	# Variable setup
	delay = 35*60  # 35 minute delay #TODO: set this delay to 35 min
	antennaVoltageCheckWait = 22*60*60 # 22 hour wait for the voltage to increase past the threshold. This is arbitrary for now
	boot = True
	saveObject = saveTofiles.save()
	# startTXISR(save)
	ttncData = getDriverData.TTNCData(saveObject)
	attitudeData = getDriverData.AttitudeData(saveObject)
	# safeModeObject = safe.safe(saveObject)
	transmitObject = Transmitting(codeBase, cameraObj)
	packet = packetProcessing(transmitObject, cameraObj)
	heartBeatObj = heart_beat()
	antennaDoorObj = antennaDoor()
	
	print('Starting data collection') #Setting up Background tasks for BOOT mode
	tasks=[]
	tasks.append(asyncio.create_task(heartBeatObj.heartBeatRun()))  # starting heart beat
	tasks.append(asyncio.create_task(pythonInterrupt.interrupt(transmitObject, packet)))  # starting rx monitoring 
	tasks.append(asyncio.create_task(ttncData.collectTTNCData(0)))  # Boot Mode is classified as 0
	tasks.append(asyncio.create_task(attitudeData.collectAttitudeData()))  # collecting attitude data

	# Initialize all mission mode objects
	# NOTE: the comms-tx is the only exception to this rule as it is to be handled differently than other mission modes
	# NOTE: Boot Mode is defined and executed in this document, instead of a separate mission mode
	# safeModeObject was deleted below in the init parameters after saveObject 
	antennaDeploy = antennaMode(saveObject, transmitObject, packet)
	preBoomDeploy = preBoomMode(saveObject, transmitObject, packet)
	postBoomDeploy = postBoomMode(saveObject, transmitObject, packet)
	boomDeploy = boomMode(saveObject, transmitObject, cameraObj, packet)

	# Check the boot record if it doesn't exist recreate it 
	if(readData() == (None, None, None)):
		print('Files are empty')
		bootCount, antennaDeployed, lastMode = 0,False,0
	# otherwise save the last mission mode
	else:
		bootCount, antennaDeployed, lastMode = readData()  
	bootCount += 1  # Increment boot count
	# save data
	recordData(bootCount, antennaDeployed, lastMode)

	if lastMode not in range(0,7): #Mission Mode invalid
		lastMode = 0
		antennaDeployed = False
	
	recordData(bootCount, antennaDeployed, lastMode)

	# This is the implementation of the BOOT mode logic.
	if not antennaDeployed:  # First, sleep for 35 minutes
		print('Antenna is undeployed, waiting 35 minutes')
		await asyncio.sleep(delay)  # Sleep for 35 minutes
		while(transmitObject.isRunning()):
			await asyncio.sleep(60) #sleep if a transmission is running

	print("Moving on to check antenna door status")
	#deploy the antenna, if it fails we will do nothing
	eps = EPS()
	voltageCount = 0
	try: 
		while True:
			try :
				BusVoltage = eps.getBusVoltage()
			except :
				#if we fail to check the bus voltage we will set it to the max value plus one
				BusVoltage = 5.1 + 1
			if antennaDeployed == True:
				break
			elif (not antennaDeployed) and (BusVoltage > 3.75):
				antennaDoorObj.deployAntennaMain() #wait for the antenna to deploy
				await asyncio.sleep(300)
				break
			elif ((antennaVoltageCheckWait/10) < voltageCount):
				antennaDoorObj.deployAntennaMain() #wait for the antenna to deploy
				await asyncio.sleep(300)
				break
			else:
				voltageCount += 1
				await asyncio.sleep(10)
	except :
		print("____Failed to deploy the antenna_____")
	# status is set True if all 4 doors are deployed, else it is False
	try:
		status = antennaDoorObj.readDoorStatus()
	except:
		status = False
		print("Failed to check antenna door status")
	if antennaDeployed == True:
		pass
	elif status == True:
		antennaDeployed = True
	else:
		antennaDeployed = False

	recordData(bootCount, antennaDeployed, lastMode)

	
	try:  # Cancels attitude collection tasks
		for t in tasks:
			t.cancel()
		print('Successfully cancelled BOOT mode background tasks')
	except asyncio.exceptions.CancelledError:
		print("Exception thrown cancelling task - This is normal")
		
	if not antennaDeployed:
		await asyncio.gather(antennaDeploy.run())
		print('Running Antenna Deployment Mode')
		antennaDeployed = True
		print("Antenna Deployed = ", antennaDeployed)
		recordData(bootCount, antennaDeployed, lastMode)  # Save into files
	elif lastMode == 4:
		print('Running Post Boom Deploy')
		lastMode = 4
		recordData(bootCount, antennaDeployed, lastMode)  # Save into files
		await asyncio.gather(postBoomDeploy.run())
	else:
		print('Running preBoom Deploy')
		lastMode = 2
		recordData(bootCount, antennaDeployed, lastMode)  # Save into files
		await asyncio.gather(preBoomDeploy.run())
		lastMode = 3
		recordData(bootCount, antennaDeploy, lastMode)
		print("Finished running preBoomDeploy")


	while True: # This loop executes the rest of the flight logic
	# pre boom deploy
		print("Entered the loop that chooses the next mission mode.")
		recordData(bootCount, antennaDeployed, lastMode)  # Save into files
		if ((antennaDeployed == True) and (lastMode != 3) and (lastMode != 4)):
			print('Running pre-Boom deploy')
			lastMode = 2
			recordData(bootCount, antennaDeployed, lastMode)
			await asyncio.gather(preBoomDeploy.run())  # Execute pre-boom deploy, then move to post-boom deploy
			print("Finished preBoomDeploy")
			lastMode = 3
			recordData(bootCount, antennaDeployed, lastMode)
		elif ((antennaDeployed == True) and (lastMode == 3)):
			print('Running Boom Deploy')
			await asyncio.gather(boomDeploy.run())  # Execute boom deployment, start post-boom deploy
			lastMode = 4
			recordData(bootCount, antennaDeployed, lastMode)
		else:  # Post-Boom Deploy
			print('Running post-Boom Deploy')
			recordData(bootCount, antennaDeployed, lastMode)  # Save into files
			await asyncio.gather(postBoomDeploy.run())


def recordData(bootCount, antennaDeployed, lastMode):
	# write to the boot file, "w" option in write overwrites the file
	fileChecker.checkFile("/home/pi/flightLogicData/bootRecords.txt")
	new = open("/home/pi/flightLogicData/bootRecords.txt", "w+")
	new.write(str(bootCount) + '\n')
	if antennaDeployed:
		new.write(str(1)+'\n')
	else:
		new.write(str(0)+'\n')
	new.write(str(lastMode) + '\n')
	new.close()

	# write to the the back up file
	fileChecker.checkFile("/home/pi/flightLogicData/backupBootRecords.txt")
	new = open("/home/pi/flightLogicData/backupBootRecords.txt", "w+")
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
	fileChecker.checkFile("/home/pi/flightLogicData/bootRecords.txt")
	try:
		bootFile = open("/home/pi/flightLogicData/bootRecords.txt", "r")
		bootCount = int(bootFile.readline().rstrip())
		antennaDeployed = bool(int(bootFile.readline().rstrip()))
		lastMode = int(bootFile.readline().rstrip())
		bootFile.close()
	except:
		try:
			print('File exception')
			fileChecker.checkFile("/home/pi/flightLogicData/backupBootRecords.txt")
			bootFile = open("/home/pi/flightLogicData/backupBootRecords.txt", "r")
			bootCount = int(bootFile.readline().rstrip())
			antennaDeployed = bool(int(bootFile.readline().rstrip()))
			lastMode = int(bootFile.readline().rstrip())
			bootFile.close()
			# In this except statement, the files are corrupted, so we rewrite both of them
		except:
			print('Double File exception - are both files non-existant?')	
			fileChecker.checkFile("/home/pi/flightLogicData/bootRecords.txt")
			bootFile = open("/home/pi/flightLogicData/bootRecords.txt", "w")
			fileChecker.checkFile("/home/pi/flightLogicData/backupBootRecords.txt")
			backupBootFile = open("/home/pi/flightLogicData/backupBootRecords.txt", "w")
			bootFile.write('0\n0\n0\n')
			backupBootFile.write('0\n0\n0\n')

	recordData(bootCount, antennaDeployed, lastMode)
	return bootCount, antennaDeployed, lastMode

async def heartBeat(): #Sets up up-and-down voltage on pin 40 (GPIO 21) for heartbeat with Arduino
		waitTime = 4
		while True:
			GPIO.output(21, GPIO.HIGH)
			print("Heartbeat wave high")
			await asyncio.sleep(waitTime/2)
			GPIO.output(21, GPIO.LOW)
			print("Heartbeat wave low")
			await asyncio.sleep(waitTime/2)
