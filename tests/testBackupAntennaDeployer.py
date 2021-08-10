import sys
sys.path.append('../')
import time
from Drivers.backupAntennaDeployer import BackupAntennaDeployer
import asyncio

print("WARNING THIS WILL DEPLOY THE ANTENNA!!!!") 
for i in range(10):
    print("Count down: ", 10 - i)
    time.sleep(1)
antennaDeployTest = BackupAntennaDeployer()
asyncio.run(antennaDeployTest.deployPrimary())
print('Primary Done')
asyncio.run(antennaDeployTest.deploySecondary())
