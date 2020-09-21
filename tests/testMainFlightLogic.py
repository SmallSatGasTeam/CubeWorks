import sys
import asyncio
sys.path.append('../')
from flightLogic import mainFlightLogic
#log = open("../logs/mainLog.log", "w")
#sys.stdout = log
#sys.stderr = log
print("Flight Logic Start")
asyncio.run(mainFlightLogic.executeFlightLogic())
