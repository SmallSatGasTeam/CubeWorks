def int4tobin(num):
	#takes a 4 byte int, returns a binary representation of it
	return str(format(num, '08b'))[-8:]

def int1tobin(num):
	#takes a 1 byte integer, returns a binary representation of it
	return str(format(num, '02b'))[-2:]

def int2tobin(num):
	#takes a 2 byte integer, returns a binary representation of it
	return str(format(num, '04b'))[-4:]

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
	commandsList.append(input('Input 0 for disable TX, 1 for enable TX: '))
	for command in commandsList:
		if command == '0':
			content += command
		else:
			content += '1'
	content += '0'
	print(hex(int(content, 2))[2:].zfill(2))


