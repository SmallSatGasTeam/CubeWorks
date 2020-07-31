"""
This code is designed to test the Arduino Beetle Watchdog Command system to shut down the pi for a chosen period of time.
"""
import sys
from time import sleep
import smbus
sys.path.append('../watchdog/Heartbeat')
from Heartbeat import longTap

bus = smbus.SMBus(1)

address = 0x08

def writeNumber(value):
    bus.write_byte(address, value)

if __name__ == "__main__":
    while True:
        valueInput = input("Choose shut down time in minutes 1,2,3: ")    
        value = int(valueInput)
        writeNumber(value)

