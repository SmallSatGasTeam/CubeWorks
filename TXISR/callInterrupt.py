import asyncio
from interrupt import INTERRUPT

async def testInterrupt():
	interruptObject = INTERRUPT()
	tasks = []
	print("calling the task in interrupt")
	tasks.append(asyncio.create_task(interruptObject.watchTxWindows(1)))
	tasks.append(asyncio.create_task(interruptObject.watchReceptions()))
	while True:
		await asyncio.sleep(60)

asyncio.run(testInterrupt())

