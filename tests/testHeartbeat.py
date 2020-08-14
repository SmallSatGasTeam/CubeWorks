import sys
sys.path.append("../")
import asyncio
from flightLogic.missionModes import safe

safeMode = safe()
asyncio.run(safeMode.heartbeat())

