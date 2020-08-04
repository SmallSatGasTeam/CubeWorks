import serial
import os 
import sys
TRANSMIT_EXE = "./a.out"

print("beging")  
ser = serial.Serial ("/dev/ttyAMA0")  
print("Opening port")    
ser.baudrate = 115200                   
os.system(TRANSMIT_EXE + " 1") 
print("\nPython Reading")                     
data = ser.read(100)
print(data)                      
ser.close() 