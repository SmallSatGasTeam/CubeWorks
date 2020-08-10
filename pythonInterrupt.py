import serial
import asyncio

async def readSerial():
	serialport = serial.Serial('/dev/serial0', 115200)
	while True:
		if serialport.in_waiting:
			print(serialport.read(10))
			#data = serialport.read_until('\r')
			#print(data)
			await asyncio.sleep(5)
		else:
			print('buffer empty')
			await asyncio.sleep(5)

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
