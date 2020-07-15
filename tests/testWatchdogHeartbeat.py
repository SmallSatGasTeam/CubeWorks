<<<<<<< HEAD
import sys
sys.path.append("../")
from watchdog.Heartbeat import Heartbeat

Heartbeat.setUp()
Heartbeat.longTap()
=======
"""
This code is designed to test the Arduino Beetle Watchdog
"""
import sys
sys.path.append('../watchdog/Heartbeat')
from Heartbeat import longTap

# Run the heartbeat code that sends a pulse every 4 seconds
print("Sending the heartbeat pulse every 4 seconds")
longTap()
>>>>>>> origin/FlatSat
