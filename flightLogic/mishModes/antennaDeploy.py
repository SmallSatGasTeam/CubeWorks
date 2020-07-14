import time
import Drivers.backupAntennaDeployer.BackupAntennaDeployer as antennaDeploy
import Drivers.antennaDoor.AntennaDoor as antennaStatus
import Drivers.eps.EPS as EPS
import asyncio
from safe import safe
from getDriverData import *


class antennaMode:

    def __init__(self):
        self.thresholdVoltage = 5 #Threshold voltage to deploy
        self.maximumWaitTime = 30 #Maximum time to wait for deployment before going to SAFE
        self.timeWaited = 0 #Time already waited - zero
        self.criticalVoltage = 3.3 #modify

    async def run(self):
        #Attitude Data - copied from jack's flight logic. will need to change
        ttncData = TTNCData()
        attitudeData = AttitudeData()
	asyncio.run(ttncData.collectTTNCData(), attitudeData.collectAttitudeData())
        safeMode = safe()
            
        #Check battery conditions - changed from jack's flight logic based on returning structure - will return to 
		await while True:
			epsVoltage = EPS.getBusVoltage()
			if epsVoltage < self.criticalVoltage:
                		safeMode.run(10) #1 hour
			await asyncio.sleep(1) #check voltage every second
            
        #Perform tasks for antenna deployment
        eps = EPS() #creating EPS object
        
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
