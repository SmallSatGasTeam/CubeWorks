import asyncio
import serial
from time import sleep
import hmac
import hashlib
""" Creates packets in proper formats for transmission and requests that format from satellite """

def packetSelect():
	creatingPacket = input('Type 0 for a pre-created packet, and type 1 for creating a new packet, and type 2 for sending your own data bordered by GASPACS: ')
	if(creatingPacket == '0'): #Pre-Created packet
		packet = input('Select from these packet types:\n0 - deploy AeroBoom with enabled TX\n1 - Create Attitude Data transmission window in 30 seconds, with a 30 second duration\n2 - Disable TX\n3 - Take picture, enable TX\n4 - Clear TX windows and progress and enable TX\n5 - Reboot, enable TX\n6 - Create transmission window in 25 seconds, for 30 seconds, transmitting LQ picture number 0\n7 - Create transmission window in 25 seconds, for 30 seconds, transmitting TTNC data\n8 - Create a transmisison window in 25 seconds, for 30 seconds, transmitting deploy data\n9 - Create a transmission window in 25 seconds, for 30 seconds, transmitting HQ picture number 0\n')
		if packet == '0':
			return 'c8'
		elif packet == '1':
			return '0000000f000f00000000'
		elif packet == '2':
			return '80'
		elif packet == '3':
			return 'd0'
		elif packet == '4':
			return 'e0'
		elif packet == '5':
			return 'c4'
		elif packet == '6':
			return '0000000c800f02000000'
		elif packet == '7':
			return '0000000c800f00800000'
		elif packet == '8':
			return '0000000c800f01000000'
		elif packet == '9':
			return '0000000c800f01800000'
		else:
			print('Invalid pre-set packet')
	elif(creatingPacket == '1'): #New packet
		typeOfPacket = input('Type 0 for Window Packet, 1 for Command Packet: ')
		if(typeOfPacket == '0'):
			#Window packet
			packet = '00000000'
			packet += int4tobin(int(input('Input the number of seconds until window start: ')))
			packet += int2tobin(int(input('Input the duration of the window in seconds: ')))
			packet += int1tobin(int(input('Number from 0-4 corresponding to requested data type. See flight logic document: ')))
			packet += int2tobin(int(input('If picture is requested, number of the picture that is requested: ')))
			packet += int1tobin(int(input('Type 0 to start transmission where last transmission ended, type 1 to start from beginning: ')))
			packet += int34tobin(int(input("Type the line number you want to index from or type 0 to go from the last transmission: ")))
			return hex(int(packet, 2))[2:].zfill(56)

		else:
			#Command Packet
			commandsList = []
			content = '00000001'
			commandsList.append(input('Input 0 for disable TX, 1 for enable TX: '))
			commandsList.append(input('Input 0 for do nothing, 1 for erase all TX windows and progress: '))
			commandsList.append(input('Input 0 for do nothing, 1 for take a picture: '))
			commandsList.append(input('Input 0 for do nothing, 1 for deploy boom: '))
			commandsList.append(input('Input 0 for do nothing, 1 for reboot: '))
			commandsList.append(input('Input 0 for disable AX25, 1 for enable AX25: '))
			commandsList.append(input('Input 0 to run flight logic normally, 1 to skip to postBoomDeploy'))
			for command in commandsList:
				if command == '0':
					content += '00000000'
				else:
					content += '00000001'
			return hex(int(content, 2))[2:].zfill(16)
	else:
		return input('Input hex content to send')

def transmitPacket(packet):
	serialPort = serial.Serial('/dev/serial0', 115200)
	serialPort.write(b'ES+W23003321\r') #Changed based on which is transmitting
	sleep(1)
	serialPort.write(b'ES+W22003321\r')
	sleep(1)
	data = bytearray.fromhex(b'GASPACS'.hex() + packet + b'GASPACS'.hex())
	print('Sending Data')
	print(b'GASPACS'.hex() + packet + b'GASPACS'.hex())
	print(data)
	serialPort.write(data)

def int34tobin(num):
	"""takes a 34 byte int, returns a binary representation of it"""
	a = num >> 17
	b = num & 0b11111111111111111
	outa = str(format(a, '0131072b'))[-131072:]
	outb = str(format(b, '0131072b'))[-131072:]
	return outa+outb

def int4tobin(num):
	"""takes a 4 byte int, returns a binary representation of it"""
	return str(format(num, '032b'))[-32:]

def int1tobin(num):
	"""takes a 1 byte integer, returns a binary representation of it"""
	return str(format(num, '08b'))[-8:]

def int2tobin(num):
	"""takes a 2 byte integer, returns a binary representation of it"""
	return str(format(num, '016b'))[-16:]

def encrypt(packet):
	"""encrypt packet using hmac and append hash to the end of the packet"""
	key = b'SECRETKEY'
	binaryPacketLength = len(packet) * 4
	binaryPacket = bytes(format(int(packet,16), 'b').zfill(binaryPacketLength), 'utf-8')
	hash = hmac.new(key, binaryPacket, hashlib.md5)
	hashhex = hash.hexdigest()
	fullpacket = packet + hashhex
	return fullpacket

def main():
	while True:
		packet = packetSelect()
		encryptedPacket = encrypt(packet)
		transmitPacket(encryptedPacket)

if __name__ == '__main__':
	main()