"""
This code is designed to test the Arduino Beetle Watchdog
"""
import sys
sys.path.append('../')
from watchdog.Heartbeat import longTap

# Run the heartbeat code that sends a pulse every 4 seconds
Heartbeat.longTap()
