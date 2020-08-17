import asyncio
import serial
from time import sleep

serialPort = serial.Serial('/dev/serial0', 115200)
serialPort.write(b'ES+W22003321\r') #Changed based on which is transmitting
sleep(0.2)
serialPort.write(b'ES+W23003321\r')
sleep(0.2)

while True:
	print('Input data you want to transmit over radio')
	data = input()
	if(len(data)%2 == 0):
		encodedData = bytearray.fromhex(data)
		serialPort.write(encodedData)
	else:
		print('Odd length of data - remember to put it in in  hexadecimal form')
	print(data)
