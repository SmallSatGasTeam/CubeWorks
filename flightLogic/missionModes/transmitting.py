"""
This file holds the Transmitting class which houses the readNextTransferWindow 
and transmit functions that are called in each mission mode. These are the two 
functions that are needed to transmit datafrom a mission mode so to reduce 
redundancy the code was pulled out of postBoomDeploy and moved into here so it 
could be shared by all four mission modes.
"""

import os
import sys
sys.path.append("../../")
from protectionProticol.fileProtection import FileReset
import asyncio
import time
from TXISR import prepareFiles
import subprocess
from TXISR.transmitionQueue import Queue


TRANSFER_WINDOW_BUFFER_TIME = 10
fileChecker = FileReset()
filePaths = ["/home/pi/CubeWorks0/TXISR/TXServiceCode/", "/home/pi/CubeWorks1/TXISR/TXServiceCode/", "/home/pi/CubeWorks2/TXISR/TXServiceCode/", "/home/pi/CubeWorks3/TXISR/TXServiceCode/", "/home/pi/CubeWorks4/TXISR/TXServiceCode/"]

class Transmitting:
    """
    Houses the the transmit and readNextTransfer window functions to allow each
    mission mode to transmit. Instantiated in mainFlightLogic and passed to
    each mission mode.
    """
    def __init__(self, codeBase, camObj):
        fileChecker.checkFile("/home/pi/TXISRData/transmissionFlag.txt")
        self.__transmissionFlagFile = open('/home/pi/TXISRData/transmissionFlag.txt') #you need to reboot on every tx enable disable command
        self.__txWindowsPath = ('/home/pi/TXISRData/txWindows.txt')
        fileChecker.checkFile(self.__txWindowsPath)
        self.__queue = Queue(self.__txWindowsPath)
        self.__timeToNextTXwindowVar = 3133728366
        self.__duration = -1
        self.__datatype = -1
        self.__pictureNumber = -1
        self.__index = -1
        self.__codeBase = codeBase
        self.__sendData = []
        self.__inProgress = False
        self.__nextWindow = -1
        self.__camObj = camObj
        self.__tasks = []
        #start the task in for checking transmissions
        self.__tasks.append(asyncio.create_task(self.readNextTransferWindow()))
        self.__tasks.append(asyncio.create_task(self.getReadyForWindows()))
        self.__tasks.append(asyncio.create_task(self.upDateTime()))

    async def readNextTransferWindow(self):
        """
        Pulls timeToNextWindow from the next available element in the queue
        then dequeues a transfer window once within 20 seconds of that timestamp
        """
        while True:
            print(">>> Monitoring windows <<<")
            #if close enough, prep files
            #wait until 5 seconds before, return True
            if((self.__timeToNextTXwindowVar > 10) and (self.__timeToNextTXwindowVar<40) and (not self.__inProgress)): #If next window is in 20 seconds or less
                #get the data 
                print(">>> Getting data from the queue <<<")
                #turn on tx in progress flag
                self.__inProgress = True
                #read in data and then split it
                line = self.__queue.dequeue(True)
                self.__sendData = line.split(',')
                #If sendData has the right number of members
                if self.__sendData.__len__() == 5:
                    print(self.__sendData)
                    #Assign the variables appropriately
                    self.__duration = int(self.__sendData[1])
                    self.__datatype = int(self.__sendData[2])
                    self.__pictureNumber = int(self.__sendData[3])
                    self.__index = int(self.__sendData[4])
                    if self.__datatype < 3:#Attitude, TTNC, or Deployment data respectively
                        print(">>> Preparing data 0 - 2 <<<")
                        self.__inProgress = prepareFiles.prepareData(self.__duration, self.__datatype, self.__index)
                    else:
                        print(">>> Preparing data 3 - 4 <<<")
                        print("Transimtting.py:", self.__duration, self.__datatype, self.__pictureNumber)
                        self.__inProgress = prepareFiles.preparePicture(self.__duration, self.__datatype, self.__pictureNumber, self.__index, self.__camObj)
                else:
                    self.__inProgress = False
                    print(self.__sendData)
                    print("sendData is incorrect.")
            await asyncio.sleep(5)

    #this func will get call right before the tx window is ready, it calls the c code when everything is ready
    async def getReadyForWindows (self):
        print(">>> Preparing c code <<<")
        while True:
                if (self.__timeToNextTXwindowVar <= 5) and (self.__timeToNextTXwindowVar > -5) and self.__inProgress:
                    print(">>> Calling c code <<<")
                    fileChecker.checkFile('/home/pi/TXISRData/transmissionFlag.txt')
                    self.__transmissionFlagFile.seek(0)
                    if (self.__transmissionFlagFile.readline() != "Disabled"):
                        txisrCodePath = filePaths[self.__codeBase]
                        #These two are old code that we may potentially have to come back to
                        #subprocess.Popen([txisrCodePath, str(self.__datatype)])
                        #print("We should literally be running this.")
                        startTime = time.time()
                        subprocess.Popen(['sudo', './TXService.run', str(self.__datatype)], cwd = str(txisrCodePath))
                        while(self.__duration >= time.time() - startTime):
                            print("\tWaiting for TX to finish ", self.__duration >= time.time() - startTime)
                            await asyncio.sleep(2)
                        #turn off tx in progress flag
                        print("\n\nResetting the TX Service code\n\n")
                        self.__inProgress = False
                        #os.system("cd ; cd " + str(txisrCodePath) + " ; sudo ./TXService.run " + str(self.__datatype)
                    else:
                        print("Transmission flag is not enabled")
                        #turn off tx in progress flag
                        print("\n\nResetting the TX Service code\n\n")
                        self.__inProgress = False
                await asyncio.sleep(0.1) #Check at 10Hz until the window time gap is less than 5 seconds
    

    async def upDateTime(self):
        try:
            while True :
                print(">>> Updating time to tx window <<<")
                #this will delete past windows, it should be called first
                if(self.__queue.dequeue(False) - time.time() <= -10):
                    print(">>> removing old window <<<")
                    self.__queue.dequeue(True)
                #count down the time
                #set new window if one is not inprogress
                if(not self.__inProgress):
                    print(">>> finding next window <<<")
                    self.__nextWindow = self.__queue.dequeue(False)
                #print("Last window", self.__nextWindow)
                self.__timeToNextTXwindowVar = self.__nextWindow - time.time()
                print("Time to next window:", self.__timeToNextTXwindowVar)
                await asyncio.sleep(2.5)
        except:
            print("Failed to pull window")
            await asyncio.sleep(2.5)

    def isRunning(self): #Other transmission are authorized though self.__inProgress which is set by transmissionRunning
        return self.__inProgress

    def nextTXTime(self):
        return self.__timeToNextTXwindowVar
