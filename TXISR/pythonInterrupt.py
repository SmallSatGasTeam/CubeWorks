import serial
import asyncio
import sys
sys.path.append('../')
from TXISR.packetProcessing import packetProcessing
from protectionProticol.fileProtection import FileReset
from time import sleep


fileChecker = FileReset()

"""
This file sets up the interrupt process. Every five seconds, the buffer of the serial port at /dev/serial0 is read.
Content is split up into AX.25 Packets, and Command Packets. The data is passed to Jack's packetProcessing.py methods.
TODO: Implement AX.25 digipeating, probably in packetProcessing.py
To defray the possibility of half a packet being in the buffer, any half-packets are stored and evaluated the next time around
"""

async def interrupt(transmitObject, packetObj):
	packet = packetObj
	fileChecker.fullReset()
	try:
		serialport = serial.Serial('/dev/serial0', 115200) #Open serial port. Currently /dev/serial0, might change to the PL011 port for flight article
	except Exception as e:
		print("Failed to open serialport. Exception:", repr(e))
		serialport = None
	leftovers = '' #Stores any half-packets for evaluation the next loop
	# leftoversEmpty = True
	gaspacsHex = str(b'GASPACS'.hex())
	while True:
		if transmitObject.isRunning():
			await asyncio.sleep(5)
			continue
		try:
			if serialport == None:
				print("Reopening serial port")
				serialport = serial.Serial('/dev/serial0', 115200) #Open serial port. Currently /dev/serial0, might change to the PL011 port for flight article
			print("Python interrupt.", serialport.in_waiting)
			if serialport.in_waiting: #If there is content in the serial buffer, read it and act on it
			#if True: #This is a testing line
				print('Data in waiting')
				data = str(serialport.read(serialport.in_waiting).hex()) #This produces a list of nibbles (half bytes)
				data = leftovers + data #Append any leftover data for evaluation

				commands = []
				commands,  leftovers = parseData(data, gaspacsHex)
				print("Commands:" + str(commands))

				for command in commands:
					# print(command)
					await packet.processPacket(command) #Process Command Packets
				print("Made it all the way. Leftovers: ", leftovers)
				# serialport.reset_input_buffer()
				await asyncio.sleep(5)
			else: #No contents in serial buffer
				print('buffer empty')
				await asyncio.sleep(5)
				
			# serialport.close()
		except Exception as e:
			print("Failure to run interrupt. Exception:", repr(e))
			await asyncio.sleep(5)

def parseData(data, bracket): #Takes data string, in the form of hex, from async read serial function. Spits out all AX.25 packets and GASPACS packets contained inside, as well as remaining data to be put into the leftovers
	# fileChecker.fullReset()
	try:
		searching = True
		gaspacsPackets = []
		modifiedString = data
		while searching: #Searching for packets bracketed by Hex-bytes of 'GASPACS'
			content = None
			content, modifiedString, searching = searchGASPACS(modifiedString, bracket)
			if searching:
				gaspacsPackets.append(content)

		return gaspacsPackets, modifiedString
	except Exception as e:
		print("Failed in parse Data. Error:", e)
		return 0, 0, 0


def searchGASPACS(data, str): #Must be passed as a string of hex, for both parameters
	#Finds command or window packets, bracketed by <str> in <data>. Removes the brackets and the contents in between from <data>. Returns the command contents
	# fileChecker.fullReset()
	try:
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
			modifiedString = data[endIndex+len(str):]
		return content, modifiedString, changed
	except Exception as e:
		print("Error in searchGASPACS. Error:", e)
		return 0, 0, 0

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
