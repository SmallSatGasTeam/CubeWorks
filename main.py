import asyncio

from Drivers import *
from Components import *


async def startLoop():
    context = {}
    lock = asyncio.Lock()
    await asyncio.gather(
        *[d.run(context, lock) for d in [Magnetometer(), ContextPrinter()]]
    )


asyncio.run(startLoop())
