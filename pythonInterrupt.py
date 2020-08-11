import serial
import asyncio

async def readSerial():
	serialport = serial.Serial('/dev/serial0', 115200)
	leftovers = []
	gaspacsNibbles = list(b'GASPACS'.hex())
	while True:
		if serialport.in_waiting:
			data = list(serialport.read(serialport.inWaiting()).hex()) #This produces a list of nibbles (half bytes)
			data = leftovers.extend(data)
			fixes = findOccurences(''.join(data), ''.join(gaspacsNibbles))
			await asyncio.sleep(5)
		else:
			print('buffer empty')
			await asyncio.sleep(10)

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
