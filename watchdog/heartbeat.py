import asyncio
import RPi.GPIO as GPIO

async def heartbeat():
	waitTime = 4
	while True:
		GPIO.output(40, GPIO.HIGH)
		await asyncio.sleep(waitTime/2)
		GPIO.output(40, GPIO.LOW)
		await asyncio.sleep(waitTime/2)

if __name__ == '__main__':
	asyncio.run(heartbeat())
