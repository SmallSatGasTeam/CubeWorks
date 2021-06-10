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
    def __init__(self, codeBase):
        fileChecker.checkFile("/home/pi/TXISRData/transmissionFlag.txt")
        self.__transmissionFlagFile = open('/home/pi/TXISRData/transmissionFlag.txt')
        self.__txWindowsPath = ('/home/pi/TXISRData/txWindows.txt')
        fileChecker.checkFile(self.__txWindowsPath)
        self.__queue = Queue(self.__txWindowsPath)
        self.__timeToNextTXwindowVar = 3133728366
        self.__nextWindowTime = -1
        self.__duration = -1
        self.__datatype = -1
        self.__pictureNumber = -1
        self.__index = -1
        self.__codeBase = codeBase
        self.__sendData = []
        self.__inProgress = False


    async def readNextTransferWindow(self):
        """
        Pulls timeToNextWindow from the next available element in the queue
        then dequeues a transfer window once within 20 seconds of that timestamp
        """
        while True:
            print("INSIDE TRANSFER WINDOW")
            #read the given transfer window file and extract the data for the soonest transfer window
            soonestWindowTime = 0

            #while timestamp < currenttimestamp
            while (self.__queue.dequeue(0) < time.time()) and (self.__queue.dequeue(0) != -1):
                fileChecker.windowProtection()
                self.__queue.dequeue(1)
            #20 seconds before
            if ((self.__queue.dequeue(0) - time.time() <= 20) and 
                (self.__data == []) and (self.__queue.dequeue(0) > 0) 
                and (not self.__inProgress)):
                #pull the packet
                fileChecker.windowProtection()
                line = self.__queue.dequeue(1)
                self.__sendData = line.split(',')
            #If not within 20 seconds of the next time stamp
            elif ((self.__timeToNextTXwindowVar < 0) or (self.__timeToNextTXwindowVar > 20)) and (self.__queue.dequeue(0) != -1):
                #Reset data and sendData lists, pull the time till next window from the next element in the queue
                fileChecker.windowProtection()
                self.__sendData = []

            #If sendData has the right number of members
            if self.__sendData.__len__() == 5:
                print(self.__sendData)
                #Assign the variables appropriately
                try :
                    self.__timeToNextTXwindowVar = float(self.__sendData[0]) - time.time()
                    self.__duration = int(self.__sendData[1])
                    self.__datatype = int(self.__sendData[2])
                    self.__pictureNumber = int(self.__sendData[3])
                    self.__nextWindowTime = float(self.__sendData[0])
                    self.__index = int(self.__sendData[4])
                except :
                    print("Data window is unreadable")
            else:
                print("sendData is empty.")

            if (not self.__inProgress) and (self.__sendData != []):
                asyncio.tasks.create_task(self.transmissionRunning())

            await asyncio.sleep(5)
    
    async def transmit(self):
        """
        Prepares data to be sent once under 14 seconds and then runs 
        TXService.run once under 5 seconds to transmit the prepared data.
        """
        while True:
            while True:
                print("Transmit time to next window:", self.__timeToNextTXwindowVar)
                #if close enough, prep files
                #wait until 5 seconds before, return True
                if (self.__timeToNextTXwindowVar != -1) and (self.__timeToNextTXwindowVar < 15) and (self.__timeToNextTXwindowVar >= 0):
                    if self.__datatype < 3: #Attitude, TTNC, or Deployment data respectively
                        prepareFiles.prepareData(self.__duration, self.__datatype, self.__index)
                    else:
                        print("Transimtting.py:", self.__duration, self.__datatype, self.__pictureNumber)
                        prepareFiles.preparePicture(self.__duration, self.__datatype, self.__pictureNumber, self.__index)
                    break
                 #I decearsed the wait time because we were missing windows.
                await asyncio.sleep(5)
            while True:
                #print("Is it time?")
                #I added a neg time buff as well incase we are a little late gettering here
                if (self.__timeToNextTXwindowVar <= 5) and (self.__timeToNextTXwindowVar > -5):
                    fileChecker.checkFile('/home/pi/TXISRData/transmissionsFlag.txt')
                    self.__transmissionFlagFile.seek(0)
                    if self.__transmissionFlagFile.readline() == 'Enabled':
                        txisrCodePath = filePaths[self.__codeBase]
                        #These two are old code that we may potentially have to come back to
                        #subprocess.Popen([txisrCodePath, str(self.__datatype)])
                        #print("We should literally be running this.")
                        subprocess.Popen(['sudo', './TXService.run', str(self.__datatype)], cwd = str(txisrCodePath))
                        #os.system("cd ; cd " + str(txisrCodePath) + " ; sudo ./TXService.run " + str(self.__datatype)
                        break
                    else:
                        print("Transmission flag is not enabled")

                await asyncio.sleep(.01)

    async def transmissionRunning(self): #Check if a transmission is running.
        self.__inProgress = True
        await asyncio.sleep(self.__duration + 5)
        self.__inProgress = False

    async def upDateTime(self):
        #count down the time
        if (self.__queue.dequeue(0) != -1):
            self.__timeToNextTXwindowVar = self.__queue.dequeue(0) - time.time()
        #other wise set the time to the defualt vaule
        elif (self.__queue.dequeue(0) == -1) and (self.__queue.dequeue(0) - time.time()) > -10:
                self.__timeToNextTXwindowVar = 3133728366
        print("Time to next window:", self.__timeToNextTXwindowVar)
        await asyncio.sleep(2.5)

    def isRunning(self): #Other transmission are authorized though self.__inProgress which is set by transmissionRunning
        return self.__inProgress
