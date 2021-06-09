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
        if self.__queue.dequeue(0) != -1:
            self.__timeToNextWindow = self.__queue.dequeue(0)
        else:
            self.__timeToNextWindow = -1
        self.__nextWindowTime = -1
        self.__duration = -1
        self.__datatype = -1
        self.__pictureNumber = -1
        self.__index = -1
        self.__codeBase = codeBase
        self.__data = []
        self.__sendData = []
        self.__inProgress = False


    async def readNextTransferWindow(self):
        """
        Pulls timeToNextWindow from the next available element in the queue
        then dequeues a transfer window once within 20 seconds of that timestamp
        """
        while True:
            print("INSIDE TRANSFER WINDOW")
                            
            #20 seconds before
            if ((self.__queue.dequeue(0) - time.time() <= 20) and 
                (self.__data == []) and (self.__queue.dequeue(0) > 0) 
                and (not self.__inProgress)):
                #pull the packet
                line = self.__queue.dequeue(1)
                self.__data = line.split(',')
                self.__timeToNextWindow = self.__timeToNestWindow - time.time()
                await asyncio.sleep(5)
            #If not within 20 seconds of the next time stamp
            elif ((self.__timeToNextWindow < 0) or (self.__timeToNextWindow > 20)) and (self.__queue.dequeue(0) != -1):
                self.__data = []
                self.__sendData = []
                #Reset data and sendData lists, pull the time till next window from the next element in the queue
            if(self.__queue.dequeue(0) > 0):
                self.__timeToNextWindow = self.__queue.dequeue(0) - time.time()
            else :
                self.__timeToNextWindow = 3133728366
            elif self.__queue.dequeue(0) == -1:
                self.__timeToNextWindow = 3133728366


            #data[0] = time of next window, data[1] = duration of window, data[2] = datatype, data[3] = picture number, data[4] = line index
            print(self.__data)
            try:
                #If the data list isn't empty
                if self.__data != []:
                    print(float(self.__data[0]), float(self.__data[0]) - time.time(), TRANSFER_WINDOW_BUFFER_TIME)
                    #If the time to next window is less than 10
                    if(float(self.__data[0]) - time.time() > TRANSFER_WINDOW_BUFFER_TIME): #If the transfer window is at BUFFER_TIME milliseconds in the future
                       self.__sendData = self.__data
            except Exception as e:
                print("Error measuring transfer window:", e)

            #If sendData has the right number of members
            if self.__sendData.__len__() == 5:
                print(self.__sendData)
                #Assign the variables appropriately
                self.__timeToNextWindow = float(self.__sendData[0]) - time.time()
                self.__duration = int(self.__sendData[1])
                self.__datatype = int(self.__sendData[2])
                self.__pictureNumber = int(self.__sendData[3])
                self.__nextWindowTime = float(self.__sendData[0])
                self.__index = int(self.__sendData[4])
            else:
                print("sendData is empty.")

            if (not self.__inProgress) and (self.__sendData != []):
                asyncio.tasks.create_task(self.transmissionRunning())

            print("Time to next window:", self.__timeToNextWindow)
            await asyncio.sleep(5)
    
    async def transmit(self):
        """
        Prepares data to be sent once under 14 seconds and then runs 
        TXService.run once under 5 seconds to transmit the prepared data.
        """
        while True:
            while True:
                print("Transmit time to next window:", self.__timeToNextWindow)
                #if close enough, prep files
                #wait until 5 seconds before, return True
                if (self.__timeToNextWindow != -1) and (self.__timeToNextWindow < 14) and (self.__timeToNextWindow >= 0):
                    if self.__datatype < 3: #Attitude, TTNC, or Deployment data respectively
                        prepareFiles.prepareData(self.__duration, self.__datatype, self.__index)
                    else:
                        print("Transimtting.py:", self.__duration, self.__datatype, self.__pictureNumber)
                        prepareFiles.preparePicture(self.__duration, self.__datatype, self.__pictureNumber, self.__index)
                    break
                 #I decreased the wait time because we were missing windows.
                await asyncio.sleep(5)
            while True:
                #I added a negative time buffer as well incase we are a little late getting here
                if (self.__timeToNextWindow <= 5) and (self.__timeToNextWindow > -5):
                    fileChecker.checkFile('/home/pi/TXISRData/transmissionsFlag.txt')
                    self.__transmissionFlagFile.seek(0)
                    if self.__transmissionFlagFile.readline() == 'Enabled':
                        txisrCodePath = filePaths[self.__codeBase]
                        #These two are old code that we may potentially have to come back to
                        #subprocess.Popen([txisrCodePath, str(self.__datatype)])
                        subprocess.Popen(['sudo', './TXService.run', str(self.__datatype)], cwd = str(txisrCodePath))
                        #os.system("cd ; cd " + str(txisrCodePath) + " ; sudo ./TXService.run " + str(self.__datatype))
                        self.__timeToNextWindow = -1
                        break
                    else:
                        print("Transmission flag is not enabled")

                await asyncio.sleep(.01)

    async def transmissionRunning(self):
        self.__inProgress = True
        await asyncio.sleep(self.__duration + 5)
        self.__inProgress = False

    def isRunning(self):
        return self.__inProgress

    def timeToNextWindow(self):
        return self.__timeToNextWindow
