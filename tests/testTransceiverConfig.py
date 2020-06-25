import sys
sys.path.append('../')
from Drivers.transceiverConfig import TransceiverConfig
radio = TransceiverConfig()
radio.setBeaconOn()
