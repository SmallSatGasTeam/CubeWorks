import serial
import os 
import sys
TRANSMIT_EXE = "./a.out"

print("beging")  
ser = serial.Serial ("/dev/ttyAMA0")  
print("Opening port")    
ser.baudrate = 9600                   
os.system(TRANSMIT_EXE + " 1") 
print("\nsending")                     
data = ser.read()
print(data)                      
ser.close() 