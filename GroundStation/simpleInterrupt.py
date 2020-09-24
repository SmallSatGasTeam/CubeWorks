import serial
import asyncio
import sys
import os
sys.path.append('../')
import struct
from binascii import hexlify

async def simpleInterrupt():
	serialport = serial.Serial('/dev/serial0', 115200) #Open serial port. Currently /dev/serial0, might change to the PL011 port for flight article as it is currently using Mini-UART
	leftovers = '' #Stores any half-packets for evaluation the next loop
	leftoversEmpty = True
	gaspacsHex = str(b'GASPACS'.hex())
	dataFile = open(os.path.join(os.path.dirname(__file__), 'pictureData.bin'), 'wb')
	counter = 0
	while True:
		if serialport.in_waiting: #If there is content in the serial buffer, read it and act on it
			counter = 0
			data = serialport.read(serialport.in_waiting).hex() #This produces a list of nibbles (half bytes)
			print('Data: ' + str(data))
			dataFile.write(bytearray.fromhex(data))
		else: #No contents in serial buffer
			counter +=1
			print(counter)
			if(counter>25):
				break
			await asyncio.sleep(1)

if __name__ == '__main__':
	asyncio.run(simpleInterrupt())
