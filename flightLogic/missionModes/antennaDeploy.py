import time
import Drivers.backupAntennaDeployer.BackupAntennaDeployer as antennaDeploy
import Drivers.antennaDoor.AntennaDoor as antennaStatus
import Drivers.eps.EPS as EPS
import asyncio
from safe import safe
from getDriverData import *


class antennaMode:

    def __init__(self, saveobject):
        self.thresholdVoltage = 5 #Threshold voltage to deploy
        self.maximumWaitTime = 30 #Maximum time to wait for deployment before going to SAFE
        self.timeWaited = 0 #Time already waited - zero
        self.criticalVoltage = 3.3 #modify
        self.__getDataTTNC = getDriverData.TTNCData(saveobject)
		self.__getDataAttitude = getDriverData.AttitudeData(saveobject)

    async def run(self):
        ttncData = self.__getDataTTNC.TTNCData()
        attitudeData = self.__getDataAttitude.AttitudeData()
	    asyncio.run(ttncData.collectTTNCData(1), attitudeData.collectAttitudeData()) #Antenna Deploy is mission mode 1
        safeMode = safe()
	    asyncio.run(safeMode.thresholdCheck()) #Check battery conditions, run safe mode if battery drops below safe level 
	    eps = EPS() #creating EPS object    

        #Perform tasks for antenna deployment
        await while True:
            if (eps.getBusVoltage()>self.thresholdVoltage):
                antennaDeploy.deploy()
                if doorStatus == (0,0,0,0): #probably need to change this to actually work
                    #Doors are open
                    return True
            else:
                if(self.timeWaited > self.maximumWaitTime):
                    safeMode.run(10) #1 hour
                else:
                    #Wait 1 minute
                    self.timeWaited = self.timeWaited+1
                    await asyncio.sleep(60)
