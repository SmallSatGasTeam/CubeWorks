import sys
sys.path.append('../')
from Drivers.transceiverConfig import TransceiverConfig
from time import sleep
radio = TransceiverConfig()
print("Set Beacon On")
radio.setBeaconOn()
print("Wait 2.5 minutes")
sleep(150)
print("Set Beacon Off")
radio.setBeaconOff()
print("Set Low Power Mode")
radio.setLowPowerMode
sleep(60)
print("Turn off Low Power Mode with any ESTTC command")
radio.setBeaconOff()
print("Done")
