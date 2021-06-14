import asyncio
import RPi.GPIO as GPIO

class heart_beat:
    def __init__(self) -> None:
        asyncio.create_task(self.heartBeat())

    async def heartBeat(self): #Sets up up-and-down voltage on pin 40 (GPIO 21) for heartbeat with Arduino
        waitTime = 4
        while True:
            GPIO.output(21, GPIO.HIGH)
            print("Heartbeat wave high")
            await asyncio.sleep(waitTime/2)
            GPIO.output(21, GPIO.LOW)
            print("Heartbeat wave low")
            await asyncio.sleep(waitTime/2)