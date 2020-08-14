import sys
sys.path.append('../')
from Drivers.backupAntennaDeployer import BackupAntennaDeployer
import asyncio

antennaDeployTest = BackupAntennaDeployer()
asyncio.run(antennaDeployTest.deploy())

