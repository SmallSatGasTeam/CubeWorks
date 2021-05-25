import os
import sys
sys.path.append("../../")
from protectionProticol.fileProtection import FileReset
import asyncio
import time
from TXISR import prepareFiles
import subprocess
import linecache
from TXISR.transmitionQueue import Queue


TRANSFER_WINDOW_BUFFER_TIME = 10
fileChecker = FileReset()
filePaths = ["/home/pi/CubeWorks0/TXISR/TXServiceCode/", "/home/pi/CubeWorks1/TXISR/TXServiceCode/", "/home/pi/CubeWorks2/TXISR/TXServiceCode/", "/home/pi/CubeWorks3/TXISR/TXServiceCode/", "/home/pi/CubeWorks4/TXISR/TXServiceCode/"]


class Transmitting:
    def __init__(self, codeBase):
        self.__timeToNextWindow = -1
        self.__nextWindowTime = -1
        self.__duration = -1
        self.__datatype = -1
        self.__pictureNumber = -1
        self.__index = -1
        fileChecker.checkFile("/home/pi/TXISRData/transmissionFlag.txt")
        self.__transmissionFlagFile = open('/home/pi/TXISRData/transmissionFlag.txt')
        self.__txWindowsPath = ('/home/pi/TXISRData/txWindows.txt')
        fileChecker.checkFile(self.__txWindowsPath)
        self.__codeBase = codeBase
        self.__data = []
        self.__queue = Queue(self.__txWindowsPath)

    async def readNextTransferWindow(self):
        while True:
            print("INSIDE TRANSFER WINDOW")
            #read the given transfer window file and extract the data for the soonest transfer window
            fileChecker.checkFile(self.__txWindowsPath)
            transferWindowFile = open(self.__txWindowsPath)
            sendData = []
            soonestWindowTime = 0

            #This is old code
            # line = self.__transferWindowFile.readline()
            # self.__data = line.split('c')

            # for lines in transferWindowFile:
            #     print("INSIDE OF THE NEW CODE:", lines)
            #     flag = True
            #     data = lines.split(",")
            #     if (data != ['']) and (float(data[0]) > time.time()):
            #         print("DATA IS NOT EMPTY")
            #         for items in self.__queue:
            #             print("CHECKING WITH QUEUE")
            #             try:
            #                 if float(data[0]) == float(items[0]):
            #                     print("TIMESTAMP ALREADY EXISTS")
            #                     items = data
            #                     flag = False
            #                     break
            #             except Exception as e:
            #                 print("ERROR:", e)
            #         if flag:
            #             print("PUSHING TO THE HEAP")
            #             heapq.heappush(self.__queue, data)
            #     else:
            #         print("DATA IS:", data, "THIS WAS VIEWED AS EITHER EMPTY OR SMALLER THAN THE CURRENT TIMESTAMP")

            # transferWindowFile.close()
            # print(self.__queue)

            # if ((self.__nextWindowTime < time.time()) and (self.__queue.__len__() > 0)) or (self.__nextWindowTime != float(self.__queue[0][0])):
            #     print("GETTING NEW TRANSFER WINDOW FROM THE HEAP")
            #     self.__data = heapq.heappop(self.__queue)

            while (self.__nextWindowTime < time.time()) and (self.__data != ['']):
                line = self.__queue.dequeue()
                self.__data = line.split(',')
                if(self.__data != ['']):
                    self.__nextWindowTime = float(self.__data[0])

            #data[0] = time of next window, data[1] = duration of window, data[2] = datatype, data[3] = picture number, data[4] = line index
            print("About to hit try.")
            try:
                if (self.__data != ['']) or (self.__data != []):
                    print(float(self.__data[0]), float(self.__data[0]) - time.time(), TRANSFER_WINDOW_BUFFER_TIME)
                    if(float(self.__data[0]) - time.time() > TRANSFER_WINDOW_BUFFER_TIME): #If the transfer window is at BUFFER_TIME milliseconds in the future
                        if(soonestWindowTime == 0) or (float(self.__data[0]) - time.time()):
                            soonestWindowTime = float(self.__data[0]) - time.time()
                            sendData = self.__data
            except Exception as e:
                print("Error measuring transfer window:", e)

            if sendData.__len__() == 5:
                print(sendData)
                self.__timeToNextWindow = float(sendData[0]) - time.time()
                self.__duration = int(sendData[1])
                self.__datatype = int(sendData[2])
                self.__pictureNumber = int(sendData[3])
                self.__nextWindowTime = float(sendData[0])
                self.__index = int(sendData[4])
            else:
                print("sendData is empty.")

            print("Time to next window:", self.__timeToNextWindow)
            await asyncio.sleep(3)
    
    async def transmit(self):
        while True:
            while True:
                print("Transmit time to next window:", self.__timeToNextWindow)
                #if close enough, prep files
                #wait until 5 seconds before, return True
                if (self.__timeToNextWindow != -1) and (self.__timeToNextWindow < 14):
                    if self.__datatype < 3: #Attitude, TTNC, or Deployment data respectively
                        prepareFiles.prepareData(self.__duration, self.__datatype, self.__index)
                        print("Preparing data")
                    else:
                        prepareFiles.preparePicture(self.__duration, self.__datatype, self.__pictureNumber)
                    break
                await asyncio.sleep(5)
            windowTime = self.__nextWindowTime
            while True:
                if (windowTime-time.time()) <= 5:
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