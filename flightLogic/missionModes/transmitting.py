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


    async def readNextTransferWindow(self):
        while True:
            print("INSIDE TRANSFER WINDOW")
            #read the given transfer window file and extract the data for the soonest transfer window
            soonestWindowTime = 0
            print("First one", (self.__queue.dequeue(0) - time.time() <= 20), (self.__data == []), (self.__queue.dequeue(0) > 0))
            print("timeToNextWindow at the beginning of the next TransferWindow", self.__timeToNextWindow)

            #while timestamp < currenttimestamp
            while (self.__queue.dequeue(0) < time.time()) and (self.__queue.dequeue(0) != -1):
                print("Deleting old time stamps.")
                self.__queue.dequeue(1)
            #20 seconds before
            if (self.__queue.dequeue(0) - time.time() <= 20) and (self.__queue.dequeue(0) != -1) and (self.__data == []) and (self.__queue.dequeue(0) > 0):
                #pull the packet
                print("Pulling a packet.")
                line = self.__queue.dequeue(1)
                self.__data = line.split(',')
            elif (((self.__timeToNextWindow - time.time()) < 0) or ((self.__timeToNextWindow - time.time()) > 20)) and (self.__queue.dequeue(0) != -1):
                print("Time to next window is less than 20 but greater than 0")
                self.__timeToNextWindow = self.__queue.dequeue(0) - time.time()
                self.__data = []
                self.__sendData = []

            #data[0] = time of next window, data[1] = duration of window, data[2] = datatype, data[3] = picture number, data[4] = line index
            print("About to hit try.")
            print(self.__data)
            print("Second one", (self.__queue.dequeue(0) - time.time() <= 20), (self.__data == []))
            try:
                if (self.__data != ['']) or (self.__data != []):
                    print(float(self.__data[0]), float(self.__data[0]) - time.time(), TRANSFER_WINDOW_BUFFER_TIME)
                    if(float(self.__data[0]) - time.time() > TRANSFER_WINDOW_BUFFER_TIME): #If the transfer window is at BUFFER_TIME milliseconds in the future
                        if(soonestWindowTime == 0) or (float(self.__data[0]) - time.time()):
                            soonestWindowTime = float(self.__data[0]) - time.time()
                            self.__sendData = self.__data
            except Exception as e:
                print("Error measuring transfer window:", e)

            if self.__sendData.__len__() == 5:
                print(self.__sendData)
                self.__timeToNextWindow = float(self.__sendData[0]) - time.time()
                self.__duration = int(self.__sendData[1])
                self.__datatype = int(self.__sendData[2])
                self.__pictureNumber = int(self.__sendData[3])
                self.__nextWindowTime = float(self.__sendData[0])
                self.__index = int(self.__sendData[4])
            else:
                print("sendData is empty.")

            print("Time to next window:", self.__timeToNextWindow)
            await asyncio.sleep(5)
    
    async def transmit(self):
        while True:
            while True:
                print("Transmit time to next window:", self.__timeToNextWindow)
                #if close enough, prep files
                #wait until 5 seconds before, return True
                if (self.__timeToNextWindow != -1) and (self.__timeToNextWindow < 14):
                    print("Self.__timeToNextWindow is less than 14.")
                    if self.__datatype < 3: #Attitude, TTNC, or Deployment data respectively
                        prepareFiles.prepareData(self.__duration, self.__datatype, self.__index)
                        print("Preparing data")
                    else:
                        prepareFiles.preparePicture(self.__duration, self.__datatype, self.__pictureNumber)
                    break
                await asyncio.sleep(5)
            while True:
                if (self.__timeToNextWindow <= 5) and (self.__timeToNextWindow > 0):
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

    def timeToNextWindow(self):
        return self.__timeToNextWindow