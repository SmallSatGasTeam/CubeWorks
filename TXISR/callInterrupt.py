import asyncio
from interrupt import INTERRUPT


asyncio.run(testInterrupt())

async def testInterrupt():
	interruptObject = INTERRUPT()
	tasks = []
	print("calling the task in interrupt")
	tasks.append(asyncio.create_task(interruptObject.watchTxWindows()))
	tasks.append(asyncio.create_task(interruptObject.watchReceptions()))
	while True:
		await asyncio.sleep(60)

