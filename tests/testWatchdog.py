"""
This code is designed to test the Arduino Beetle Watchdog
"""
sys.path.append('../')
from watchdog.Heartbeat import Hearbeat

# Run the heartbeat code that sends a pulse every 4 seconds
Heartbeat.longTap()
