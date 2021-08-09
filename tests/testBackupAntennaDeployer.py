import sys
sys.path.append('../')
from Drivers.backupAntennaDeployer import BackupAntennaDeployer
import asyncio

print("WARNING THIS WILL DEPLOY THE ANTENNA!!!!") 
for i in range(10):
    print("Count down: ", 10 - i)
antennaDeployTest = BackupAntennaDeployer()
asyncio.run(antennaDeployTest.deployPrimary())
print('Primary Done')
asyncio.run(antennaDeployTest.deploySecondary())
