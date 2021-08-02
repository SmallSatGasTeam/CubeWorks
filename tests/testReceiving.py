import serial
import sys
from time import sleep
sys.path.append('../')

def receive():
    serialport = serial.Serial('/dev/serial0', 115200)

    while True:
        print(serialport.in_waiting, "objects in waiting.")
        
        if serialport.in_waiting:
            print("Data in waiting")
            data = serialport.read(serialport.in_waiting)
            print("Received: ", data)
        

        sleep(1)

receive()
