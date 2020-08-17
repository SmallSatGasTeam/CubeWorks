import struct

typeOfPacket = input('Type 0 for Window Packet, 1 for Command Packet')
if(typeOfPacket == '0'):
	#Window packet
	pass
else:
	#Command Packet
	commandsList = []
	commandsList.append(input('Input 0 for disable TX, 1 for enable TX'))
	commandsList.append(input('Input 0 for disable TX, 1 for enable TX'))
	commandsList.append(input('Input 0 for disable TX, 1 for enable TX'))
	commandsList.append(input('Input 0 for disable TX, 1 for enable TX'))
	commandsList.append(input('Input 0 for disable TX, 1 for enable TX'))
	commandsList.append(input('Input 0 for disable TX, 1 for enable TX'))
	commandsList.append(input('Input 0 for disable TX, 1 for enable TX'))
	commandsList.append(input('Input 0 for disable TX, 1 for enable TX'))
	clearTX = input('Input 0 for do nothing, 1 for erase all TX windows and progress')
	takePicture = input('Input 0 for do nothing, 1 for take a picture')
	deployBoom = input('Input 0 for do nothing, 1 for deploy boom')
	reboot = input('Input 0 for do nothing, 1 for reboot')
	enableAX25 = input('Input 0 for do nothing, 1 for erase all TX windows and progress')
	clearTX = input('Input 0 for do nothing, 1 for erase all TX windows and progress')








def float4tohex(num):
	#takes a 4 byte float, returns a hex representation of it
	return str(hex(struct.unpack('<I', struct.pack('<f', num))[0]))[2:]

def int4tohex(num):
	#takes a 4 byte int, returns a hex representation of it
	return str(format(num, '08x'))[-8:]

def int1tohex(num):
	#takes a 1 byte integer, returns a hex representation of it
	return str(format(num, '02x'))[-2:]

def int2tohex(num):
	#takes a 2 byte integer, returns a hex representation of it
	return str(format(num, '04x'))[-4:]

def int8tohex(num):
	#takes an 8 byte integer, returns a hex representation of it
	return str(format(num, '016x'))[-16:]
