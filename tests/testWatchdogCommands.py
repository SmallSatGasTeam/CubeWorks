"""
This code is designed to test the Arduino Beetle Watchdog Command system to shut down the pi for a chosen period of time.
"""
import sys
sys.path.append('../')
from flightLogic.missionModes import safe
if __name__ == "__main__":
	safeMode = safe.safe()
	print('Sending reboot command to arduino for 3 minutes')
	safeMode.run(3)
