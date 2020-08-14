import sys
sys.path.append('../')
from Drivers.backupAntennaDeployer import BackupAntennaDeployer
import asyncio

antennaDeployTest = BackupAntennaDeployer()
asyncio.run(antennaDeployTest.deployPrimary())
print('Primary Done')
asyncio.run(antennaDeployTest.deploySecondary())
