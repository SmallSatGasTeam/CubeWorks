import asyncio
from interrupt import INTERRUPT


asyncio.run(executeFlightLogic())


async def executeFlightLogic(): 
    interruptObject = INTERRUPT()
