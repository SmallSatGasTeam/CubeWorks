import serial
import asyncio
import sys
sys.path.append('../')
import watchdog.Heartbeat.Heartbeat as heartbeat

async def receive():
    heartbeat.setUp()
    asyncio.create_task(heartbeat.longTap())

    serialport = serial.Serial('/dev/serial10', 115200)

    while True:
        print(serialport.in_waiting(), "objects in waiting.")
        
        if serialport.in_waiting:
            print("Data in waiting")
            data = serialport.read_all()
            print("Received: ", data)
        
        await asyncio.sleep(.5)

receive()