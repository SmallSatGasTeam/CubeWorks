import serial
ser = serial.Serial ("/dev/ttyAMA0")    
ser.baudrate = 9600                   
ser.write(str.encode("hello"))                       
data = ser.read(5)
print(data)                      
ser.close() 