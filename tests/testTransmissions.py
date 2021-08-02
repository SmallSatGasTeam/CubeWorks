### This file is intended to test a simple transmission between two transceivers. Run 'cat /dev/serial0' on the receiving system, and this code on the transmitting system ###
import serial
from time import sleep
ser = serial.Serial('/dev/serial0', 115200)
# Put local radio in pipe mode. 3361 turns on pipe mode and enables AX.25 beacon.
ser.write(b'ES+W22003621') 
# Sleep for 120 ms between packets
sleep(.120)
# Put remote radio in pipe mode. 3321 turns on pipe mode, disables AX.25 beacon.
ser.write(b'ES+W23003321') 
sleep(.120)
ser.write(b'Hello There') 
ser.close()
