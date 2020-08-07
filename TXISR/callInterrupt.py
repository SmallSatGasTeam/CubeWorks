import asyncio
from TXISR.interrupt import INTERRUPT

def __main__():
	asyncio.run(executeFlightLogic())


async def executeFlightLogic(): 
    interruptObject = INTERRUPT()
