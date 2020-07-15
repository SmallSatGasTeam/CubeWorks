#NOTE: this code will not work until the TXISR branch is merged into flightLogic, but as of right now (1:00 pm 7/11/2020)
#   the txisr is not ready, however finail testing begains today, and it is expected to be done by the endo of the day,
#   or tuseday at the latest.

#this is the main file where everything happens. 
#this code will check to see which entry conditions are met and then call and run the corresponding flight mode
import mishModes 
from asyncio import *
#this imports the file we need from the TXISR
from TXISR import interrupt
from getDriverData import *
import time
import Drivers.antennaDoor as antennaDoor

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
Dealy = 126000 #seconds that we are going to delay. (total of 35 mins)
bootCount = 0
firstBoot = 0
antennaDeployed = 0
lastMode = 0
boot = True

def __main__():
    main()

def main ():
    #start txisr
    startTXISR()

    #start data collection for boot mode
    getAttitude()
    getTTNC()

    #initialize all mission mode
    #the mission mode should be named like the following
    #antenna Deploy = antennaDeployed
    #boot = boot
    #pre-boom deploy = preboomDeploy
    #post boom deploy = postBoomDeploy
    #boom delpoy = boomDeploy
    #NOTE: all mission modes should have a run() func defined, this all the this code will call, so run must 
    #   handle all necesary parts of the code
    #NOTE: the comms-tx is the only exception to this rule as it is to be handled diffrently then other mission
    #   modes. 
    #NOTE: boot logic will be defined in this doc, as it is easier just to write it here. This is because boot
    #   must be call the antenna deploy mission mode 
    antennaDeploy = mishModes.antennaDeployed()
    preboomDeploy = mishModes.preboomDeploy()
    postBoomDeploy = mishModes.postBoomDeploy()
    boomDeploy = mishModes.boomDeploy()

    #bootRecords file format
    #Line 1 = boot count
    #Line 2 = first boot?
    #Line 3 = antenna deployed?
    #Line 4 = last mission mode
    #the try except is a why to back up our files if one get correputed then we will read from
    #anthor file and recreate the first
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
        #recreate the files, beacuse if we get here there has been some type of correpution on the main boot file. 
        recordData()
    
    #NOTE: how should we handle the first boot, if we are going to do anything
    if firstBoot :
        firstBoot = False
        recordData()
    
    #add to the boot count
    bootCount += 1
    recordData()
    #this is the boot mode, beacues boot should only happen on start up it is best to leave it out of the loop
    #however should we decided that this is not the case we can put it in the loop with no problems
    #IMPORTANT NOTE: How are we going to check to make sure that we in space to deloy here?
    #AKA: so we dont deploy in the the box.
    if not antennaDeployed :
        #delay for 35 mins #change to 35
        startTime = time.time()
        currentTime =time.time()
        while((startTime - currentTime) < Dealy):
            currentTime = time.time()

        #how do we check if the antenna doors are open?
        #TODO, check of antenna doors are open
        doorOpen = True
        status = antennaDoor.readDoorStauts()
        #this checks the bytes returned by the antennaDoor if any are 0 then doorOpen gets set to false
        if not status & 0xf0:
            doorOpen = False
        if doorOpen :
            #this test to see if we have deployed the antenna correctly or not
            #NOTE: will antennaDeploy fail if it cannot deploy the antenna or should
            #   we have it return a value? (T/F)
            antennaDeploy.run()
            antennaDeployed = True
            #save it into the files
            recordData()
    elif lastMode == "post boom deploy" :
        postBoomDeploy.run()
    else :
        preboomDeploy.run()
    #turn off boot mode, which will stop collecting data
    boot = False

    #this loop will check the mission modes the rest of the mission modes to keep things running.
    while True :
        if antennaDeployed == True and lastMode != "post boom deploy":
            lastMode = "pre boom deploy"
            recordData()
            #if successful move on to next mission mode
            if(preboomDeploy.run()):
                #once we finish this mode it is time to got to post boom deploy
                lastMode = "boom deploy"
                recordData()
        elif antennaDeployed == True and lastMode == "boom deploy":
            lastMode = "boom deploy"
            recordData()
            #if successful move on to next mission mode
            if(boomDeploy.run()):
                #once we finish it is time to satrt post boom deploy mode
                lastMode = "post boom deploy"
                recordData()
            

        



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
def startTXISR():
    #this sets up the interupt on the uart pin that triggers when we get commincation over uart
    thread.start(interrupt.watchReceptions)

##################################################################################################################
#get ttnc 
##################################################################################################################
#gets the ttnc data for boot mode
#it does so every 120 milliseconds
##################################################################################################################
async def  getTTNC() :
    ttnc = TTNCData()
    startTime = round(time.tiem() * 1000) #this is to get the milliseconds
    while True:
        currentTime = round(time.tiem() * 1000)
        #boot is a flag that is set when the program starts, once we leave boot mode it is set to false and we
        #stop collecting the datta
        if not boot:
            break;     
        #this will let us wait 120 milliseconds untill we get the data again. 
        if((startTime - currentTime) == 120) :
            startTime = round(time.tiem() * 1000)
            ttnc.getData()

##################################################################################################################
#get attitude
##################################################################################################################
#gets the attitude data,
#it does so once persecond
##################################################################################################################
async def getAttitude() :
    attitude= AttitudeData()
    while True:
        #boot is a flag that is set when the program starts, once we leave boot mode it is set to false and we
        #stop collecting the datta
        if not boot:
            break;  
        attitude.getData()   
        #this will let us wait 1 seconds untill we get the data again.    
        await asyncio.sleep(1) 
