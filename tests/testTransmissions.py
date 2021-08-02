### This file is intended to test a simple transmission between two transceivers. On the receiving system run 'stty -F /dev/serial0 115200' and then 'cat /dev/serial0' ###
import serial
from time import sleep
ser = serial.Serial('/dev/serial0', 115200)
# Put local radio in pipe mode. 3361 turns on pipe mode and enables AX.25 beacon.
ser.write(b'ES+W22003361\r') 
# Sleep for 120 ms between packets
sleep(.120)
# Put remote radio in pipe mode. 3321 turns on pipe mode, disables AX.25 beacon.
print("1")
ser.write(b'ES+W23003321\r') 
sleep(.120)
ser.write(b'Hello There 0\r') 
sleep(.120)
ser.write(b'Hello There 1\r') 
sleep(.120)
ser.write(b'Hello There 2\r') 
sleep(.120)
ser.write(b'Hello There 3\r') 
sleep(.120)
ser.write(b'Hello There 4\r') 
sleep(.120)
ser.write(b'Hello There 5\r') 
sleep(.120)
ser.write(b'Hello There 6\r') 
sleep(.120)
ser.write(b'Hello There 7\r') 
sleep(.120)
ser.write(b'Hello There 8\r') 
sleep(.120)
ser.write(b'Hello There 9\r') 
ser.close()
