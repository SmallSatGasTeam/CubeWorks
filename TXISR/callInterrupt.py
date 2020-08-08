import asyncio
from interrupt import INTERRUPT

async def testInterrupt():
	interruptObject = INTERRUPT()
	while true :
		if interruptObject.getRXSTatous() :
			print("Starting RX watching")
			asyncio.create_task(interruptObject.watchReceptions())
		if interruptObject.getTXstatus() :
			#syncio.create_task(interruptObject.watchTxWindows())


asyncio.run(testInterrupt())

