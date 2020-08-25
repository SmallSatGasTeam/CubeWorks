import asyncio
import serial
from time import sleep

def packetSelect():
	creatingPacket = input('Type 0 for a pre-created packet, and type 1 for creating a new packet')
	if(creatingPacket == '0'): #Pre-Created packet
		packet = input('Select from these packet types:\n0 - deploy AeroBoom\n1 - Create Attitude Data transmission window in 30 seconds, with a 30 second duration\n')
		if packet == '0':
			return 'c8'
		elif packet == '1':
			return '0000000f000f00000000'
		else:
			print('Invalid pre-set packet')
	else: #New packet
		typeOfPacket = input('Type 0 for Window Packet, 1 for Command Packet: ')
		if(typeOfPacket == '0'):
			#Window packet
			packet = '0'
			packet += int4tobin(int(input('Input the number of seconds until window start: ')))
			packet += int2tobin(int(input('Input the duration of the window in seconds: ')))
			packet += int1tobin(int(input('Number from 0-4 corresponding to requested data type. See flight logic document: ')))
			packet += int2tobin(int(input('If picture is requested, number of the picture that is requested: ')))
			packet += '0000000'
			print(hex(int(packet, 2))[2:].zfill(20))

		else:
			#Command Packet
			commandsList = []
			content = '1'
			commandsList.append(input('Input 0 for disable TX, 1 for enable TX: '))
			commandsList.append(input('Input 0 for do nothing, 1 for erase all TX windows and progress: '))
			commandsList.append(input('Input 0 for do nothing, 1 for take a picture: '))
			commandsList.append(input('Input 0 for do nothing, 1 for deploy boom: '))
			commandsList.append(input('Input 0 for do nothing, 1 for reboot: '))
			commandsList.append(input('Input 0 for disable AX25, 1 for enable AX25: '))
			for command in commandsList:
				if command == '0':
					content += command
				else:
					content += '1'
			content += '0'
			return hex(int(content, 2))[2:].zfill(2)

def transmitPacket(packet):
	serialPort = serial.Serial('/dev/serial0', 115200)
	serialPort.write(b'ES+W22003321\r') #Changed based on which is transmitting
	sleep(0.2)
	serialPort.write(b'ES+W23003321\r')
	sleep(0.2)
	data = bytearray.fromhex(b'GASPACS'.hex() + packet + b'GASPACS'.hex())
	serialPort.write(encodedData)


def int4tobin(num):
	#takes a 4 byte int, returns a binary representation of it
	return str(format(num, '032b'))[-32:]

def int1tobin(num):
	#takes a 1 byte integer, returns a binary representation of it
	return str(format(num, '08b'))[-8:]

def int2tobin(num):
	#takes a 2 byte integer, returns a binary representation of it
	return str(format(num, '016b'))[-16:]

def main():
	while True:
		packet = packetSelect()
		transmitPacket(packet)

if __name__ == '__main__':
	main()




