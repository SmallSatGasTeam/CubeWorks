import asyncio
from interrupt import INTERRUPT

def __main__():
	asyncio.run(executeFlightLogic())


async def executeFlightLogic(): 
    interruptObject = INTERRUPT()
