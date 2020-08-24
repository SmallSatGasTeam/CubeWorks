import sys
sys.path.append('../')
from Drivers.transceiverConfig import TransceiverConfig

radio = TransceiverConfig()
radio.writeData(b'ES+W23003321\r')
radio.writeData(b'ES+W22003321')
sleep(.15)
radio.writeData(b'Hello there\r')
