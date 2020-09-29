import serial
import asyncio
import sys
import os
sys.path.append('../')
import struct
import datetime

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
	filePath = 'Data/Attitude_Data/Attitude_Data ' + str(datetime.datetime.now()) + '.txt'
	dataFile = open(os.path.join(os.path.dirname(__file__), filePath), 'a+')
	print(filePath)
	while True:
		if serialport.in_waiting: #If there is content in the serial buffer, read it and act on it
			print('Data in waiting')
			data = str(serialport.read(serialport.in_waiting).hex()) #This produces a list of nibbles (half bytes)
			data = leftovers+data #Append any leftover data for evaluation
			if leftovers != '':
				leftoverEmpty = False
			commands, ax25Packets = [], []
			commands, ax25Packets, leftovers = parseData(data, gaspacsHex)
			if leftovers != '' and leftoversEmpty == False:
				#Something is sticking around in leftovers, let's clear it
				#Operates on the assumption that 2 consecutive partial packets is practically impossible
				print('Leftover bits in buffer: ' + leftovers)
				leftovers = ''
			for command in commands:
				if command is not '':
					print('Data bordered by GASPACS in hex:' + command)
					decodeData(command, dataFile)
				else:
					print('Empty packet failure')
					return True

			for ax25 in ax25Packets:
				#Process AX.25 Packets
				print('AX.25 packet: ' + command)
			await asyncio.sleep(0.01)
		else: #No contents in serial buffer
			print('buffer empty')
			await asyncio.sleep(0.05)


def decodeData(data, dataFile):
	#data is a string of hex bytes
	#Decode data, store raw data and decoded data in a file
	packetType = data[0:2]
	dataContent = []
	if packetType == '00': #Attitude Data
		dataContent.append(0) #Datatype 0
		dataContent.append(intFromHex(data[2:10])) #Timestamp, int 4
		dataContent.append(floatFromHex(data[10:18])) #Sun-Sensor 1, float 4
		dataContent.append(floatFromHex(data[18:26])) #Sun-Sensor 2, float 4
		dataContent.append(floatFromHex(data[26:34])) #Sun-Sensor 3, float 4
		dataContent.append(floatFromHex(data[34:42])) #Sun-Sensor 4, float 4
		dataContent.append(floatFromHex(data[42:50])) #Sun-Sensor 5, float 4
		dataContent.append(floatFromHex(data[50:58])) #Magnetic field x, float 4
		dataContent.append(floatFromHex(data[58:66])) #Magnetic field y, float 4
		dataContent.append(floatFromHex(data[66:74])) #Magnetic field z, float 4
	elif packetType == '01': #TT&C Data
		dataContent.append(1) #Datatype 1
		dataContent.append(intFromHex(data[2:10])) #Timestamp, int 4
		dataContent.append(intFromHex(data[10:12])) #Mission mode, int 1
		dataContent.append(intFromHex(data[12:16])) #Reboot count, int 2
		dataContent.append(floatFromHex(data[16:24])) #Boombox uv, float 4
		dataContent.append(floatFromHex(data[24:32])) #SPX+ temp, float 4
		dataContent.append(floatFromHex(data[32:40])) #SPZ+ temp, float 4
		dataContent.append(floatFromHex(data[40:48])) #CPU temp, float 4
		dataContent.append(floatFromHex(data[48:56])) #EPS MCU temp, float 4
		dataContent.append(floatFromHex(data[56:64])) #Cell 1 battery temp, float 4
		dataContent.append(floatFromHex(data[64:72])) #Cell 2 battery temp, float 4
		dataContent.append(floatFromHex(data[72:80])) #Battery voltage, float 4
		dataContent.append(floatFromHex(data[80:88])) #Battery current, float 4
		dataContent.append(floatFromHex(data[88:96])) #BCR voltage, float 4
		dataContent.append(floatFromHex(data[96:104])) #BCR current, float 4
		dataContent.append(floatFromHex(data[104:112])) #EPS 3v3 current, float 4
		dataContent.append(floatFromHex(data[112:120])) #EPS 5v current, float 4
		dataContent.append(floatFromHex(data[120:128])) #SPX voltage, float 4
		dataContent.append(floatFromHex(data[128:136])) #SPX+ current, float 4
		dataContent.append(floatFromHex(data[136:144])) #SPX- current, float 4
		dataContent.append(floatFromHex(data[144:152])) #SPY voltage, float 4
		dataContent.append(floatFromHex(data[152:160])) #SPY+ current, float 4
		dataContent.append(floatFromHex(data[160:168])) #SPY- current, float 4
		dataContent.append(floatFromHex(data[168:176])) #SPZ voltage, float 4
		dataContent.append(floatFromHex(data[176:184])) #SPZ+ current, float 4
	else: #Deployment Data
		dataContent.append(2) #Datatype 2
		dataContent.append(intFromHex(data[2:18])) #Timestamp in ms, int 8
		dataContent.append(floatFromHex(data[18:26])) #Boombox UV, float 4
		dataContent.append(floatFromHex(data[26:34])) #Acceleration x, float 4
		dataContent.append(floatFromHex(data[34:42])) #Acceleration y, float 4
		dataContent.append(floatFromHex(data[42:50])) #Acceleration z, float 4

	dataFile.write('Raw Data: ' + str(data) + '\n')
	dataFile.write('Decoded Data in List Format: ' + str(dataContent) + '\n\n')

	print('Raw Data: ' + str(data) + '\n')
	print('Decoded Data in List Format: ' + str(dataContent) + '\n\n')

def parseData(data, bracket): #Takes data string, in the form of hex, from async read serial function. Spits out all AX.25 packets and GASPACS packets contained inside, as well as remaining data to be put into the leftovers
	searching = True
	gaspacsPackets = []
	ax25Packets = []
	modifiedString = data
	while searching: #Searching for packets bracketed by Hex-bytes of 'GASPACS'
		content = None
		content, modifiedString, searching = searchGASPACS(modifiedString, bracket)
		if searching:
			gaspacsPackets.append(content)

	searching = True
	while searching: #Searching for packets bracketed by AX.25 header and footer, as described in Endurosat UHF Transceiver II User Manual Rev. 1.8
		content = None
		content, modifiedString, searching = searchAX25(modifiedString)
		if searching:
			ax25Packets.append(content)

	return gaspacsPackets, ax25Packets, modifiedString

def searchAX25(data): #Finds AX.25 packets stored in the data string, which is a string of hex. Removes it from data, returns AX.25 packet and modified data
	prefix = '7e7e7e7e7e7e7e7e7e'
	postfix = '7e7e7e7e'
	changed = False
	modifiedString = ''
	content = []
	startIndex = data.find(prefix)
	endIndex = data.find(postfix)
	if startIndex != -1:
		#AX25 prefix exists
		endIndex = data.find(postfix, startIndex+17)
		if endIndex != -1:
			#Both exist
			content = data[startIndex:endIndex+len(postfix)]
			changed = True
			modifiedString = data[0:startIndex] + data[endIndex+len(postfix):]
	return content, modifiedString, changed


def searchGASPACS(data, str): #Must be passed as a string of hex, for both parameters
	#Finds command or window packets, bracketed by <str> in <data>. Removes the brackets and the contents in between from <data>. Returns the command contents
	content=''
	occurences = findOccurences(data, str)
	modifiedString = data
	changed = False
	i=0
	if (0<len(occurences)-1):
		changed = True
		startIndex = occurences[i]+len(str)
		endIndex = occurences[i+1]
		content = (data[startIndex:endIndex])
		modifiedString = data[0:startIndex-len(str)] + data[endIndex+len(str):]
	return content, modifiedString, changed

def findOccurences(str1, str2): #Finds all occurences of String 2 in String 1, returns a list of all the indices where String 2 appeared
	occurenceList = []
	minIndex = 0
	while True:
		foundIndex = str1.find(str2, minIndex)
		if(foundIndex != -1):
			minIndex = foundIndex + 1
			occurenceList.append(foundIndex)
		else:
			break
	return occurenceList

def intFromHex(hex):
	return int(hex, 16)

def floatFromHex(hex):
	return struct.unpack('!f', bytes.fromhex(hex))[0]
def main():
	asyncio.run(interrupt())

if __name__ == '__main__':
	main()
