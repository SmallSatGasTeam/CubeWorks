import asyncio
from interrupt import INTERRUPT

def __main__():
	asyncio.run(testInterrupt)

async def testInterrupt():
	interruptObject = INTERRUPT()
	tasks = []
	tasks.append(asyncio.create_task(interruptObject.watchTxWindows()))
	tasks.append(asyncio.create_task(interruptObject.watchReceptions()))
	while True:
		await asyncio.sleep(60)
