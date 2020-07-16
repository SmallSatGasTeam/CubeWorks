import asyncio
import time

async def printOne():
	while True:
		print("printOne running, every 2 seconds")
		await asyncio.sleep(2)

async def printTwo():
	while True:
		print("printTwo running, every 3 seconds")
		await asyncio.sleep(3)

async def printBoth():
	asyncio.gather(printOne(), printTwo())
	print("sleeping, running both functions for 15 seconds")
	await asyncio.sleep(15)
	print("DONE, STOPPING TASKS")
	stopAll()

def stopAll():
	pendingTasks = asyncio.all_tasks()
	for task in pendingTasks:
		task.cancel()
