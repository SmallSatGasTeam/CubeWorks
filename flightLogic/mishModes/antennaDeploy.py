import time
import Drivers.backupAntennaDeployer.BackupAntennaDeployer as antennaDeploy
import Drivers.antennaDoor.AntennaDoor as antennaStatus


class antennaMode:

    def __init__(self):
        '''
           TODO:
               Figure out how to get the following values (they are not zero). some may be contained in the main file
               via the "context" variable in missionLogic.py.
        '''
        self.timeOut = 0
        self.epsValue = 0
        self.timeOut = 0
        self.critPower = 0

    def run(self):

        timeElapsed = 0  # this will be minuets. if timeElapsed = 3 that means 3 minutes

        while timeElapsed < self.timeOut:
            if self.epsValue > self.critPower:
                if antennaStatus.readDoorStatus == False:
                    self.deployment()
                else:
                    return -1  # this is supposed to be a flag saying that the antennas are deployed
            else:
                time.sleep(60)
                timeElapsed += 1
        if timeElapsed < self.timeOut:
            print("TODO: call SAFE")  # this may need to be made into a flag as well

    def deployment(self):
        antennaDeploy.deploy()

