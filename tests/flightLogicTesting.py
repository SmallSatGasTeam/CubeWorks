import sys
import asyncio
sys.path.append('../')
from flightLogic import mainFlightLogic
asyncio.run(mainFlightLogic.executeFlightLogic())
