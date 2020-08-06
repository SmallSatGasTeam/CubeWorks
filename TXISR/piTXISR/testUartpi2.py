import serial
import os 
import sys
TRANSMIT_EXE = "./a.out"
read_EXE = "./test.out"

print("beging")  
ser = serial.Serial ("/dev/ttyAMA0")  
print("Opening port")    
ser.baudrate = 115200 
checking = os.system(read_EXE) 
while not checking : 
    checking = os.system(read_EXE)
print("\nPython sending to the 1st pi")                
os.system(TRANSMIT_EXE + " 1")                     
ser.close() 