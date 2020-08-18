import serial
import asyncio
import sys
sys.path.append('../')

async def interrupt():
	serialport = serial.Serial('/dev/serial0', 115200) #Open serial port. Currently /dev/serial0, might change to the PL011 port for flight article
	leftovers = '' #Stores any half-packets for evaluation the next loop
	leftoversEmpty = True
	gaspacsHex = str(b'GASPACS'.hex())
	while True:
		if serialport.in_waiting: #If there is content in the serial buffer, read it and act on it
			data = str(serialport.read(serialport.inWaiting()).hex()) #This produces a list of nibbles (half bytes)
			data = leftovers+data #Append any leftover data for evaluation
			if leftovers is not '':
				leftoverEmpty = False
			commands, ax25Packets = [], []
			commands, ax25Packets, leftovers = parseData(data, gaspacsHex)
			for command in commands:
				print(command)
			if leftovers is not '' and leftoversEmpty is False:
				#Something is sticking around in leftovers, let's clear it
				#Operates on the assumption that 2 consecutive partial packets is practically impossible
				leftovers = ''
			await asyncio.sleep(0.5)
		else: #No contents in serial buffer
			print('buffer empty')
			await asyncio.sleep(0.5)
asyncio.run(interrupt())
