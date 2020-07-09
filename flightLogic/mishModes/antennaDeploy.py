import time
import Drivers.backupAntennaDeployer.BackupAntennaDeployer as antennaDeploy

class antennaMode:
    '''
    TODO:
        Figure out how to get these values. some will come from the main file.
    '''
    timeElapsed = 0
    timeOut = 0
    epsValue = 0
    critPower = 0

    def powerCheck(self):
        while self.timeElapsed < self.timeOut:  # not sure what that the time out is.
            if self.epsValue > self.critPower:
                self.deployment()
                return -1  # this is supposed to be a flag saying that the antennas are deployed
            else:
                time.sleep(60)
        if self.timeElapsed < self.timeOut:
            print("TODO: call SAFE")

    def deployment(self):
        antennaDeploy.deploy()

