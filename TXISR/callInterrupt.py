import asyncio
from interrupt import INTERRUPT

async def testInterrupt():
	interruptObject = INTERRUPT()
	tasks = []
	print("calling the task in interrupt")
	tasks.append(asyncio.create_task(interruptObject.watchTxWindows()))
	tasks.append(asyncio.create_task(interruptObject.watchReceptions()))

asyncio.run(testInterrupt())

