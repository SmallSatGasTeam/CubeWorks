"""
These are the classes that handle saving the data to the files

Each class has one func that will write all the data in a list that
is passed to it.

They are written as different classes so that each code my be quicker

NOTE: try to only instantiate the classes once. if you have to do
more this will not cause a  problem it will only slow the code
down.
"""
import os.path
import asyncio
import time
from protectionProticol.fileProtection import FileReset


fileChecker = FileReset()

class save:
    def __init__(self):
        pass

    #write the data to the file,
    #NOTE: it is important that you put a : after the time stamp, this will
    #effect the txisr
    async def writeTTNC(self, data):
        fileChecker.checkFile("/home/pi/flightLogicData/TTNC_Data.txt")
        TTNC_File = open('/home/pi/flightLogicData/TTNC_Data.txt', "a+")
        TTNC_File.write(str(data)+'\n')
        TTNC_File.close()


    #this is data collection for Deploy
    #write the data to the file,
    #NOTE: it is important that you put a : after the time stamp, this will
    #effect the txisr
    async def writeDeploy(self, data):
        fileChecker.checkFile("/home/pi/flightLogicData/Deploy_Data.txt")
        Deploy_File = open("/home/pi/flightLogicData/Deploy_Data.txt", "a+")
        Deploy_File.write(str(data)+'\n')
        Deploy_File.close()


    #this part of the code is for data collection of attitude data
    #write the data to the file,
    #NOTE: it is important that you put a : after the time stamp, this will
    #effect the txisr
    async def writeAttitude(self, data):
        fileChecker.checkFile("/home/pi/flightLogicData/Attitude_Data.txt")
        Attitude_File = open("/home/pi/flightLogicData/Attitude_Data.txt", "a+")
        Attitude_File.write(str(data)+'\n')
        Attitude_File.close()

