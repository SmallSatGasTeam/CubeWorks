import asyncio
from interrupt import INTERRUPT

async def testInterrupt():
	interruptObject = INTERRUPT()
	tasks = []
	tasks.append(asyncio.create_task(interruptObject.watchReceptions()))
	tasks.append(asyncio.create_task(interruptObject.watchTxWindows()))
	while true :
		if interruptObject.getRXSTatous() :
			tasks[0] = (asyncio.create_task(interruptObject.watchReceptions()))
		if interruptObject.getTXstatus() :
			#tasks[1] = (asyncio.create_task(interruptObject.watchTxWindows()))


asyncio.run(testInterrupt())

