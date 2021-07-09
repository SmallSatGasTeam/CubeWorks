import Heartbeat
import asyncio
from flightLogic.missionModes.heartBeat import heart_beat

""" Tests if heartbeat is working """

Heartbeat.setUp()
heartBeatObj = heart_beat()
print("Starting receive.")
asyncio.create_task(heartBeatObj.heartBeatRun())
