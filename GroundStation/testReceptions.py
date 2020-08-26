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
	while True:
		if serialport.in_waiting: #If there is content in the serial buffer, read it and act on it
			print('Data in waiting')
			data = str(serialport.read(serialport.in_waiting()).hex()) #This produces a list of nibbles (half bytes)
			data = leftovers+data #Append any leftover data for evaluation
			if leftovers != '':
				leftoverEmpty = False
				print('Leftovers are not empty!')
			commands, ax25Packets = [], []
			commands, ax25Packets, leftovers = parseData(data, gaspacsHex)
			if leftovers != '' and leftoversEmpty == False:
				#Something is sticking around in leftovers, let's clear it
				#Operates on the assumption that 2 consecutive partial packets is practically impossible
				print('Leftover bits in buffer: ' + leftovers)
				leftovers = ''
			for command in commands:
				print('Data bordered by GASPACS in hex:' + command)
				decodeData(command)
			for ax25 in ax25Packets:
				#Process AX.25 Packets
				print('AX.25 packet: ' + command)
			await asyncio.sleep(0.1)
		else: #No contents in serial buffer
			print('buffer empty')
			await asyncio.sleep(0.1)

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
