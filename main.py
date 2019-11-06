import asyncio

from Components import *
from Drivers import *

async def startLoop():
    context = {}
    lock = asyncio.Lock()
    drivers = [DummyMagnetometer(), ContextPrinter()]
    await asyncio.gather(*[d.run(context, lock) for d in drivers])


try:
    asyncio.run(startLoop())
except KeyboardInterrupt:
    pass
