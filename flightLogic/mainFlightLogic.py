# This is the main file, to be run on startup of the Pi
import getDriverData
import saveTofiles
import Drivers.antennaDoor.AntennaDoor as antennaDoor
import missionModes.antennaDeploy
import missionModes.preBoomDeploy
import missionModes.boomDeploy
import missionModes.postBoomDeploy
import asyncio

# from TXISR import interrupt
# NOTE: The TXISR needs to run as a separate thread, and is not asyncio
# import thread @@Shawn This import isn't working

##################################################################################################################
# executeFlightLogic()
##################################################################################################################
# First, this function sets up the TXISR and then checks the boot conditions
# Then, it runs a mission mode, and then loops forever, constantly checking to run the next mission mode.
# NOTE: Each mission mode evaluates their exit conditions to leave the mission mode.
# NOTE: Each mission mode calls safe if it is necessary
# NOTE: DO NOTE record safe mode in the bootRecords file
##################################################################################################################



def __main__():
    executeFlightLogic()


async def executeFlightLogic():  # Open the file save object, start TXISR, and start Boot Mode data collection
    # Variable setup
    delay = 2100  # 35 minute delay = 2100 second delay
    bootCount = 0
    antennaDeployed = False
    lastMode = "Boot" #Shawn, I don't know how you want this stored
    boot = True

    save = saveTofiles.save()
    #startTXISR(save)
    taskAttitude = asyncio.create_task(getAttitude())
    taskTTNC = asyncio.create_task(getTTNC())
    # Initialize all mission mode objects
    # NOTE: the comms-tx is the only exception to this rule as it is to be handled differently than other mission modes
    # NOTE: Boot Mode is defined and executed in this document, instead of a separate mission mode
    antennaDeploy = missionModes.antennaDeploy(save)
    preBoomDeploy = missionModes.preBoomDeploy(save)
    postBoomDeploy = missionModes.postBoomDeploy(save)
    boomDeploy = missionModes.boomDeploy(save)

    bootCount, antennaDeployed, lastMode = readData()  # Read in data from files
    bootCount += 1  # Increment boot count
    recordData(bootCount, antennaDeployed, lastMode)

    # This is the implementation of the BOOT mode logic.
    if not antennaDeployed:  # First, sleep for 35 minutes
        await asyncio.sleep(delay)  # Sleep for 35 minutes

    # how do we check if the antenna doors are open?
    # TODO, check of antenna doors are open
    doorOpen = True
    status = antennaDoor.readDoorStatus()
    # this checks the bytes returned by the antennaDoor if any are 0 then doorOpen gets set to false
    if not status & 0xf0:
        doorOpen = False
    else:
        antennaDeployed = True
    recordData()

    if not doorOpen:
        asyncio.create_task(antennaDeploy.run())
        antennaDeployed = True
        recordData() #Save into files
    elif lastMode == "post boom deploy":
        asyncio.create_task(postBoomDeploy.run())
    else:
        asyncio.create_task(preBoomDeploy.run())

    try:  # Cancels attitude collection tasks
        taskAttitude.cancel()
        taskTTNC.cancel()
    except asyncio.exceptions.CancelledError:
        print("Exception thrown cancelling task - normal")

    while True:  # This loop executes the rest of the flight logic
        if antennaDeployed == True and lastMode != "post boom deploy":
            lastMode = "pre boom deploy"
            recordData()
            asyncio.create_task(preBoomDeploy.run())  # Execute pre-boom deploy, then move to post-boom deploy
            lastMode = "boom deploy"
            recordData()
        elif antennaDeployed == True and lastMode == "boom deploy":
            asyncio.create_task(boomDeploy.run())  # Execute boom deployment, start post-boom deploy
            lastMode = "post boom deploy"
            recordData()
        else:  # Post-Boom Deploy
            asyncio.create_task(postBoomDeploy.run())


def recordData(bootCount, antennaDeployed, lastMode):


    # write to the boot file, "w" option in write overwrites the file
    new = open("bootRecords", "w")
    new.write(str(bootCount))
    new.write(str(antennaDeployed))
    new.write(str(lastMode))
    new.close()

    # write to the the back up file
    new = open("backupBootRecords", "w")
    new.write(str(bootCount))
    new.write(str(antennaDeployed))
    new.write(str(lastMode))
    new.close()


def readData():  # This function reads in data from the files, it was previously in the main function but is better as its own function
    # bootRecords file format
    # Line 1 = boot count
    # Line 2 = first boot
    # Line 3 = antenna deployed?
    # Line 4 = last mission mode
    # the try except is a way to back up our files, if one is corrupted the other used
    try:
        bootFile = open("bootRecords", "r")
        bootCount = int(bootFile.readline())
        antennaDeployed = bool(bootFile.readline())
        lastMode = str(bootFile.readline())
        bootFile.close()
    except:
        bootFile = open("backupBootRecords", "r")
        bootCount = int(bootFile.readline())
        antennaDeployed = bool(bootFile.readline())
        lastMode = str(bootFile.readline())
        bootFile.close()
        # In this except statement, the files are corrupted, so we rewrite both of them
        recordData()
    return bootCount, antennaDeployed, lastMode


#def startTXISR(saveobject):  # Setup for TXISR
    # This sets up the interupt on the uart pin that triggers when we get commincation over uart
    #thread.start(interrupt.watchReceptions(saveobject)) <-- TODO fix that import

# These functions collect data in the background during BOOT mode, if applicable
async def getTTNC():
    ttnc = TTNCData()
    while True:
        ttnc.getData(0)  # BOOT is mission mode 0
        await asyncio.sleep(120) #0.0083HZ


async def getAttitude():
    attitude = AttitudeData()
    while True:
        attitude.getData()
        await asyncio.sleep(1) #1HZ
