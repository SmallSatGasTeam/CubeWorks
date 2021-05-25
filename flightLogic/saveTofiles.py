#####################################################################
#This are the classes that handle saving the data to the files
#####################################################################
#Each class has one func that will write all the data in a list that
#is passed to it.
#They are written as different classes so that each code my be quicker
#NOTE: try to only instantiate the classes once. if you have to do
#more this will not cause a  problem it will only slow the code
#down.
#####################################################################
import os.path
import asyncio
import time
from protectionProticol.fileProtection import FileReset


fileChecker = FileReset()

class save:
    def __init__(self):
        #check the file to make sure it is their        
        #fileChecker.checkFile("/home/pi/flightLogicData/TTNC_Data.txt")
        #open the file when the calls is instantiated
        #self.__TTNC_File = open("/home/pi/flightLogicData/TTNC_Data.txt", "a+")
        #check the file to make sure it is their
        # fileChecker.checkFile("/home/pi/flightLogicData/Deploy_Data.txt")
        # #open the file when the calls is instantiated
        # self.__Deploy_File = open("/home/pi/flightLogicData/Deploy_Data.txt", "a+")
        # #check the file to make sure it is their
        # fileChecker.checkFile("/home/pi/flightLogicData/Attitude_Data.txt")
        # #open the file when the calls is instantiated
        # self.__Attitude_File = open("/home/pi/flightLogicData/Attitude_Data.txt", "a+")
        pass

    #write the data to the file,
    #NOTE: it is important that you put a : after the time stamp, this will
    #effect the txisr
    async def writeTTNC(self, data):
        fileChecker.checkFile("/home/pi/flightLogicData/TTNC_Data.txt")
        TTNC_File = open('/home/pi/flightLogicData/TTNC_Data.txt', "a+")
        TTNC_File.write(str(data)+'\n')
        TTNC_File.close()

    #this func will read the data from our file and then return that data
    async def getTTNC(self, time):
        fileChecker.checkFile("/home/pi/flightLogicData/TTNC_Data.txt")
        print("####CHECKING TTNC DATA")
        temp = []
        for i in self.__TTNC_File:
            if (int(i[0]) >= time):
                temp += i
        return temp

    #this is data collection for Deploy
    #write the data to the file,
    #NOTE: it is important that you put a : after the time stamp, this will
    #effect the txisr
    async def writeDeploy(self, data):
        fileChecker.checkFile("/home/pi/flightLogicData/Deploy_Data.txt")
        deployFile = open("/home/pi/flightLogicData/Deploy_Data.txt", "a+")
        deployFile.write(str(data)+'\n')
        deployFile.close()

    #this func will read the data form our file and then return that data
    async def getDeploy(self):
        fileChecker.checkFile("/home/pi/flightLogicData/Deploy_Data.txt")
        temp = []
        for i in self.__Deploy_File:
            if (int(i[0]) >= time):
                temp += i
        return temp
    #this part of the code is for data collection of attitude data
    #write the data to the file,
    #NOTE: it is important that you put a : after the time stamp, this will
    #effect the txisr
    async def writeAttitude(self, data):
        fileChecker.checkFile("/home/pi/flightLogicData/Attitude_Data.txt")
        Attitude_File = open("/home/pi/flightLogicData/Attitude_Data.txt", "a+")
        Attitude_File.write(str(data)+'\n')
        Attitude_File.close()


    #this func will read the data form our file and then return that data
    async def getAttitudeData(self):
        fileChecker.checkFile("/home/pi/flightLogicData/Attitude_Data.txt")
        temp = []
        for i in self.__Attitude_File:
            if (int(i[0]) >= time):
                temp += i
        return temp

    #this will check if it is time to tx or not and then return a bool
    #TODO: how are we saving tx times?
    def checkTxWindow(self):
        fileChecker.checkFile("/home/pi/TXISRData/txWindows.txt")
        txWindows = open("/home/pi/TXISRData/txWindows.txt")
        timeToTx = txWindows.readlines()
        for i in timeToTx:
            if (i - 10000) <= round(time.time() * 1000):
                return True
        return False
