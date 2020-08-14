import sys
sys.path.append('../')
from Drivers.boomDeployer import BoomDeployer
import asyncio

boomDeployTest = BoomDeployer()
asyncio.run(boomDeployTest.deploy())

