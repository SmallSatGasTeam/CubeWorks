import serial
import asyncio
import sys
sys.path.append('../')
from flightLogic.missionModes.heartBeat import heart_beat

async def receive():
    heartBeatObj = heart_beat()
    print("Starting receive.")
    asyncio.create_task(heartBeatObj.heartBeatRun())

    try:
        serialport = serial.Serial('/dev/serial0', 115200)
    except Exception as e:
        print("Failed, error:", e)

    print("Finished the serial port")
    while True:
        print("In the loop.")
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