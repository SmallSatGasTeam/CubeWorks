import sys
import asyncio
sys.path.append('../')
from flightLogic import DummymainFlightLogic
asyncio.run(DummymainFlightLogic.executeFlightLogic())
