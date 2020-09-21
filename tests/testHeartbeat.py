import sys
sys.path.append("../")
import asyncio
from flightLogic.missionModes import safe

safeMode = safe.safe(None)
asyncio.run(safeMode.heartBeat())

