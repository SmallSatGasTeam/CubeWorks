import serial
import os 
import sys
TRANSMIT_EXE = "./a.out"
read_EXE = "./watchRX.run"

print("beging")  
ser = serial.Serial ("/dev/ttyAMA0")  
print("Opening port")    
ser.baudrate = 115200                   
os.system(TRANSMIT_EXE + " 1") 
print("\nPython Reading") 
checking = os.system(read_EXE) 
while not checking : 
    checking = os.system(read_EXE)
    print(checking)                    
data = ser.read(100)
print(data)                      
ser.close() 