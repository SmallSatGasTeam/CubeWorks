import sys
import asyncio
sys.path.append('../')
from flightLogic import mainFlightLogic
#log = open("../logs/mainLog.log", "w")
#sys.stdout = log
#sys.stderr = log
print("Flight Logic Start\n>>>THIS IS THE SOFTWARE TESTING VERSION<<<\nEverything may not work\nPlease change the crontab file\n steps to change it\n1: sudo crontab -e\n 2: set the file to @reboot sudo runuser pi -c cd ''/home/pi/Integration/CubeWorks/tests ; python3 testMainFlightLogic.py''")
asyncio.run(mainFlightLogic.executeFlightLogic())
