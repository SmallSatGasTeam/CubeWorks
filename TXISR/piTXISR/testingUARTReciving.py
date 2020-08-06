import serial
import os 
import sys

print("beging")  
ser = serial.Serial ("/dev/ttyAMA0")  
print("Opening port")    
ser.baudrate = 115200                   
print("\nPython Reading")
while true:
    data = ser.read(100)
    print(data) 