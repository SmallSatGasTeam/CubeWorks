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

class save:
    def __init__(self):
        #open the file when the calls is instantiated
        self.__TTNC_File = open("TTNC_Data.txt", "w+")
        #open the file when the calls is instantiated
        self.__Deploy_File = open("Deploy_Data.txt", "w+")
        #open the file when the calls is instantiated
        self.__AttitudeData = open("Attitude_Data.txt", "w+")
        
    #write the data to the file,
    #NOTE: it is important that you put a : after the time stamp, this will
    #effect the txisr
    def writeTTNC(self, data):
        temp = 0
        for i in data:
            if temp == 0:
                self.__TTNC_File.write(i + ": ")
                temp += 1
            else :
                self.__TTNC_File.write(i)

    #this func will read the data form our file and then return that data
    def getTTNC(self, time):
        temp = []
        for i in self.__TTNC_File:
            if ((int) i[0] >= time):
                temp += i
        return temp
    #this is data collection for Deploy     
    #write the data to the file,
    #NOTE: it is important that you put a : after the time stamp, this will
    #effect the txisr
    def writeDeploy(self, data):
        temp = 0
        for i in data:
            if temp == 0:
                self.__TTNC_File.write(i + ": ")
                temp += 1
            else :
                self.__TTNC_File.write(i)
    #this func will read the data form our file and then return that data
    def getDeploy(self):
        temp = []
        for i in self.__Deploy_File:
            if ((int) i[0] >= time):
                temp += i
        return temp
    #this part of the code is for data collection of attitude data
    #write the data to the file,
    #NOTE: it is important that you put a : after the time stamp, this will
    #effect the txisr
    def writeAttitude(self, data):
        temp = 0
        for i in data:
            if temp == 0:
                self.__TTNC_File.write(i + ": ")
                temp += 1
            else :
                self.__TTNC_File.write(i)

    #this func will read the data form our file and then return that data
    def getAttitudeData(self):
        temp = []
        for i in self.__AttitudeData:
            if ((int) i[0] >= time):
                temp += i
        return temp