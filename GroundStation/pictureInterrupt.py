import serial
import asyncio
import sys
import os
sys.path.append('../')
import struct

"""
This file sets up the interrupt process. Every five seconds, the buffer of the serial port at /dev/serial0 is read.
Content is split up into AX.25 Packets, and Command Packets. The data is passed to Jack's packetProcessing.py methods.
TODO: Implement AX.25 digipeating, probably in packetProcessing.py
To defray the possibility of half a packet being in the buffer, any half-packets are stored and evaluated the next time around
"""
async def interrupt():
	serialport = serial.Serial('/dev/serial0', 115200) #Open serial port. Currently /dev/serial0, might change to the PL011 port for flight article as it is currently using Mini-UART
	leftovers = '' #Stores any half-packets for evaluation the next loop
	leftoversEmpty = True
	gaspacsHex = str(b'GASPACS'.hex())
	dataFile = open(os.path.join(os.path.dirname(__file__), 'pictureData.bin'), 'wb')
	while True:
		if serialport.in_waiting: #If there is content in the serial buffer, read it and act on it
			data = serialport.read(serialport.in_waiting).hex() #This produces a list of nibbles (half bytes)
			print('Data: ' + str(data))
			dataFile.write(data)
		else: #No contents in serial buffer
			print('Serial Buffer Empty')
			await asyncio.sleep(0.5)

if __name__ == '__main__':
	asyncio.run(interrupt())
