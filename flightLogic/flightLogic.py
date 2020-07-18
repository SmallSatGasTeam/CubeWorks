#NOTE: this code will not work until the TXISR branch is merged into flightLogic, but as of right now (1:00 pm 7/11/2020)
#   the txisr is not ready, however finail testing begains today, and it is expected to be done by the endo of the day,
#   or tuseday at the latest.

#this is the main file where everything happens. 
#this code will check to see which entry conditions are met and then call and run the corresponding flight mode
import missionModes
from asyncio import *
#this imports the file we need from the TXISR
from TXISR import interrupt
from getDriverData import *
import time
import Drivers.antennaDoor as antennaDoor
import saveTofiles

#NOTE: The TXISR needs to run as a separate thread, and is not asyncio
import thread

##################################################################################################################
#Main()
##################################################################################################################
#This python file is what we call when we boot, it starts off the entire process of out our flight logic.
#First thing it does is set up the TXISR
#then it check the previous boot conditions
#then it will enter into a forever loop that will constently check conditions and flags that have been set on the
#pi. It will use these conditions to decided where or not to call mission modes. 
#Once a mission mode is complete it will exit and return to the main loop which will continue to check conditions
#on the pi untill the entrence condition are meet for the next mission mode.
#NOTE: it is the job of each mission mode to eval exit conditons and decided when to leave the mission mode.
#NOTE: each mission mode is responsable for deciding to call safe if it is needed
#NOTE: DO NOTE, record safe mode in the bootRecords files this is beacuse we want the program to pick up on the 
#   same mode it left off on when it boots up again time
##################################################################################################################
delay = 2100 # 35 minute delay = 2100 second delay
bootCount = 0
firstBoot = 0
antennaDeployed = 0
lastMode = 0
boot = True

def __main__():
    main()

def main ():
    #Open the file save object, start TXISR, and start Boot Mode data collection
    save = saveTofiles.save()
    startTXISR(save)
    taskAttitude = asyncio.create_task(getAttitude())
    taskTTNC = asyncio.create_task(getTTNC())

    #Initialize all mission mode objects
    #NOTE: the comms-tx is the only exception to this rule as it is to be handled differently than other mission modes
    #NOTE: Boot Mode is defined and executed in this document, instead of a separate mission mode
    antennaDeploy = missionModes.antennaDeployed(save)
    preBoomDeploy = missionModes.preboomDeploy(save)
    postBoomDeploy = missionModes.postBoomDeploy(save)
    boomDeploy = missionModes.boomDeploy(save)

    #bootRecords file format
    #Line 1 = boot count
    #Line 2 = first boot
    #Line 3 = antenna deployed?
    #Line 4 = last mission mode
    #the try except is a way to back up our files, if one is corrupted the other used
    try :
        bootFile = open("bootRecords", "r")
        bootCount = bootFile.readline()
        firstBoot = bootFile.readline()
        antennaDeployed = bootFile.readline()
        lastMode = bootFile.readline()
        bootFile.close()
    except :
        bootFile = open("backupBootRecords", "r")
        bootCount = bootFile.readline()
        firstBoot = bootFile.readline()
        antennaDeployed = bootFile.readline()
        lastMode = bootFile.readline()
        bootFile.close()
        #In this except statement, the files are corrupted, so we rewrite both of them
        recordData()

    #@SHAWN can I delete this?? NOTE: how should we handle the first boot, if we are going to do anything
    #if firstBoot :
        #firstBoot = False
        #recordData()

    #add to the boot count
    bootCount += 1
    recordData()



    #This is the implementation of the BOOT mode logic.
    if not antennaDeployed : #First, sleep for 35 minutes
        startTime = time.time()
        currentTime = time.time()
        while((startTime - currentTime) < delay):
            currentTime = time.time()
            await asyncio.sleep(5) #Sleep for 5 seconds between checking every time, otherwise the CPU will be more active than necessary


        #how do we check if the antenna doors are open?
        #TODO, check of antenna doors are open
        doorOpen = True
        status = antennaDoor.readDoorStatus()
        #this checks the bytes returned by the antennaDoor if any are 0 then doorOpen gets set to false
        if not status & 0xf0:
            doorOpen = False
	else:
            antennaDeployed = True
            recordData()

        if not doorOpen:
            asyncio.run(antennaDeploy.run())
            antennaDeployed = True
            #save it into the files
            recordData()
    elif lastMode == "post boom deploy" :
        asyncio.run(postBoomDeploy.run())
    else:
        asyncio.run(preBoomDeploy.run())

    try: #Cancels attitude collection tasks
        taskAttitude.cancel()
        taskTTNC.cancel()
    except asyncio.exceptions.CancelledError:
        #Exception here is normal


    while True: #This loop executes the rest of the flight logic
        if antennaDeployed == True and lastMode != "post boom deploy":
            lastMode = "pre boom deploy"
            recordData()
            asyncio.run(preBoomDeploy.run()) #Execute pre-boom deploy, then move to post-boom deploy
            lastMode = "boom deploy"
            recordData()
        elif antennaDeployed == True and lastMode == "boom deploy":
            asyncio.run(boomDeploy.run()) #Execute boom deployment, start post-boom deploy
            #once we finish it is time to satrt post boom deploy mode
            lastMode = "post boom deploy"
            recordData()
        else: #Post-Boom Deploy
            asyncio.run(postBoomDeploy.run())


##################################################################################################################
#recordData()
##################################################################################################################
#records data in the back up files
##################################################################################################################
def recordData():
    #write to the boot file, 
    #NOTE: "w" errase all previous lines in the file
    new = open("bootRecords", "w")
    new.write(bootCount)
    new.write(firstBoot)
    new.write(antennaDeployed)
    new.write(lastMode)
    new.close()

    #write to the the back up file
    new = open("backupBootRecords", "w")
    new.write(bootCount)
    new.write(firstBoot)
    new.write(antennaDeployed)
    new.write(lastMode)
    new.close()


##################################################################################################################
#startTXISR()
##################################################################################################################
#sets up txisr
##################################################################################################################
def startTXISR(saveobject):
    #this sets up the interupt on the uart pin that triggers when we get commincation over uart
    thread.start(interrupt.watchReceptions(saveobject))

##################################################################################################################
#get ttnc
##################################################################################################################
#gets the ttnc data for boot mode
#it does so every 120 seconds
##################################################################################################################
async def  getTTNC() :
    ttnc = TTNCData()
    while True:
            ttnc.getData()
            await asyncio.sleep(120)

##################################################################################################################
#get attitude
##################################################################################################################
#gets the attitude data,
#it does so once per second
##################################################################################################################
async def getAttitude() :
    attitude= AttitudeData()
    while True:
        attitude.getData()
        #this will let us wait 1 seconds untill we get the data again.
        await asyncio.sleep(1)
