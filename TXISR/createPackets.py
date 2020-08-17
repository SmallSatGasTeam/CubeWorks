import struct

typeOfPacket = input('Type 0 for Window Packet, 1 for Command Packet')
if(typeOfPacket == '0'):
	#Window packet
	pass
else:
	#Command Packet
	commandsList = []
	content = '1'
	commandsList.append(input('Input 0 for disable TX, 1 for enable TX'))
	commandsList.append(input('Input 0 for do nothing, 1 for erase all TX windows and progress'))
	commandsList.append(input('Input 0 for do nothing, 1 for take a picture'))
	commandsList.append(input('Input 0 for do nothing, 1 for deploy boom'))
	commandsList.append(input('Input 0 for do nothing, 1 for reboot'))
	commandsList.append(input('Input 0 for disable TX, 1 for enable TX'))
	for command in commandsList:
		if command == '0':
			content += command
		else:
			content += '1'
	content += '0'
	print(hex(int(content, 2))[2:].zfill(2))
	







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
