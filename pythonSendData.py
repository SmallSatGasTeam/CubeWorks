import serial
import asyncio

async def writeSerial():
	serialport = serial.Serial('/dev/serial0', 115200)
	while True:
		data = 'ES+W23003321\r'.encode('utf-8')
		serialport.write(b'hello')
		print(data)
		await asyncio.sleep(.120)
		data = 'ES+W22003321\r'.encode('utf-8')
		serialport.write(data)
		print(data)
		await asyncio.sleep(.120)
		data = 'hello'.encode('utf-8')
		for i in range(0,5):
			serialport.write(data)
			print(data)
			await asyncio.sleep(.120)
		break

async def otherFunction():
	while True:
		print('Other functionalities running')
		await asyncio.sleep(1)

async def main():
	asyncio.create_task(writeSerial())
	#asyncio.create_task(otherFunction())
	while True:
		#print('even more functionality')
		await asyncio.sleep(2)

if __name__ == '__main__':
	asyncio.run(main())
