import sys
sys.path.append('../')
import asyncio
from flightLogic.missionModes.heartBeat import heart_beat

""" Tests if heartbeat is working """

heartBeatObj = heart_beat()
print("Starting receive.")
asyncio.run(heartBeatObj.heartBeatRun())
