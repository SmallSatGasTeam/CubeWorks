import serial
print("beging")  
ser = serial.Serial ("/dev/ttyAMA0")  
print("Opend port")    
ser.baudrate = 9600                   
ser.write(str.encode("hello"))  
print("sending")                     
data = ser.read(5)
print(data)                      
ser.close() 