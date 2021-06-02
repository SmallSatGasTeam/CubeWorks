import serial
import asyncio
import sys
sys.path.append('../')
import watchdog.Heartbeat.Heartbeat as heartbeat

async def receive():
    heartbeat.setUp()
    asyncio.create_task(heartbeat.longTap())

    try:
        serialport = serial.Serial('/dev/serial0', 115200)
    except Exception as e:
        print("Failed, error:", e)

    while True:
        try:
            print(serialport.in_waiting, "objects in waiting.")
            
            if serialport.in_waiting:
                print("Data in waiting")
                data = serialport.read_all()
                print("Received: ", data)
            
            await asyncio.sleep(.5)
        except Exception as e:
            print("Error:", e)

asyncio.run(receive())