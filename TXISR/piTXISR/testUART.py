import serial
print("beging")  
ser = serial.Serial ("/dev/tty1")  
print("Opening port")    
ser.baudrate = 9600                   
ser.write(str.encode("hello"))  
print("\nsending")                     
data = ser.read(5)
print(data)                      
ser.close() 