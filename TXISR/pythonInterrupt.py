import serial
import asyncio
import packetProcessing

async def readSerial():
	serialport = serial.Serial('/dev/serial0', 115200)
	leftovers = ''
	gaspacsHex = str(b'GASPACS'.hex())
	while True:
		if serialport.in_waiting:
			print('Data in waiting')
			data = str(serialport.read(serialport.inWaiting()).hex()) #This produces a list of nibbles (half bytes)
			data = leftovers+data
			commands, ax25Packets = None, None
			commands, ax25Packets, leftovers = parseData(data, gaspacsHex)
			for command in commands:
				packetProcessing.processPacket(command)
			await asyncio.sleep(1)
		else:
			print('buffer empty')
			await asyncio.sleep(1)

def parseData(data, bracket): #Takes data string, in the form of hex, from async read serial function. Spits out all AX.25 packets and GASPACS packets contained inside, as well as remaining data to be put into the leftovers
	searching = True
	gaspacsPackets = []
	ax25Packets = []
	modifiedString = data
	while searching: #searching for GASPACS-bracketed packets
		content = None
		content, modifiedString, searching = searchGASPACS(modifiedString, bracket)
		if searching:
			gaspacsPackets.append(content)

	searching = True
	print('asdf '+str(modifiedString))
	while searching:
		content = None
		content, modifiedString, searching = searchAX25(modifiedString)
		if searching:
			ax25Packets.append(content)

	return gaspacsPackets, ax25Packets, modifiedString

def searchAX25(data): #Finds AX.25 packets stored in the dat astring, which is a string of hex. Removes it from data, returns AX.25 packet and modified data
	prefix = '7e7e7e7e7e7e7e7e7e'
	postfix = '7e7e7e7e'
	changed = False
	modifiedString = ''
	content = []
	startIndex = data.find(prefix)
	endIndex = data.find(postfix)
	if startIndex is not -1:
		#AX25 prefix exists
		endIndex = data.find(postfix, startIndex+17)
		if endIndex is not -1:
			#Both exist
			content = data[startIndex:endIndex+len(postfix)]
			changed = True
			modifiedString = data[0:startIndex] + data[endIndex+len(postfix):]
	return content, modifiedString, changed


def searchGASPACS(data, str): #Must be passed as a string of hex, for both parameters
	#Finds command or window packets, bracketed by <str> in data. Removes brackets and contents, returns contents
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

def findOccurences(str1, str2):
	occurenceList = []
	minIndex = 0
	while True:
		foundIndex = str1.find(str2, minIndex)
		if(foundIndex is not -1):
			minIndex = foundIndex + 1
			occurenceList.append(foundIndex)
		else:
			break
	return occurenceList

async def otherFunction():
	while True:
		print('Other functionalities running')
		await asyncio.sleep(1)

async def main():
	asyncio.create_task(readSerial())
	#asyncio.create_task(otherFunction())
	while True:
		#print('even more functionality')
		await asyncio.sleep(2)

if __name__ == '__main__':
	asyncio.run(main())
