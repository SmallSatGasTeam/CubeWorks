import sys
sys.path.append('../')
from Drivers.transceiverConfig import TransceiverConfig

radio = TransceiverConfig()
radio.writeData("ES+W23003321")
radio.writeData("ES+W22003321")
sleep(.15)
radio.writeData("Hello there")
