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

class save:
    def __init__(self):
        #open the file when the calls is instantiated
        self.__TTNC_File = open(os.path.dirname(__file__) + "/data/TTNC_Data.txt", "a+")
        #open the file when the calls is instantiated
        self.__Deploy_File = open(os.path.dirname(__file__) + "/data/Deploy_Data.txt", "a+")
        #open the file when the calls is instantiated
        self.__Attitude_File = open(os.path.dirname(__file__) + "/data/Attitude_Data.txt", "a+")

    #write the data to the file,
    #NOTE: it is important that you put a : after the time stamp, this will
    #effect the txisr
    async def writeTTNC(self, data):
        self.__TTNC_File.write(str(data)+'\n')

    #this func will read the data from our file and then return that data
    async def getTTNC(self, time):
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
        self.__TTNC_File.write(str(data)+'\n')

    #this func will read the data form our file and then return that data
    async def getDeploy(self):
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
        self.__Attitude_File.write(str(data)+'\n')


    #this func will read the data form our file and then return that data
    async def getAttitudeData(self):
        temp = []
        for i in self.__Attitude_File:
            if (int(i[0]) >= time):
                temp += i
        return temp

    #this will check if it is time to tx or not and then return a bool
    #TODO: how are we saving tx times?
    def checkTxWindow(self):
        timeToTx = txWindows.readlines()
        for i in timeToTx:
            if (i - 10000) <= round(time.time() * 1000):
                return True
        return False
