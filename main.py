import asyncio

from Drivers import *


async def startLoop():
    context = {}
    lock = asyncio.Lock()
    await asyncio.gather(
        *[d.run(context, lock) for d in [
            Magnetometer()
        ]])


asyncio.run(startLoop())
