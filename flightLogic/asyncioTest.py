import asyncio
import time
import random
from contextlib import suppress

async def main():
	tMode = testMissionMode()
	task = await asyncio.gather(tMode.run())
	print("tMode.run() should be finished now. Waiting 5 seconds then exiting")
	await asyncio.sleep(5)
	return

class testClassOne:
	def __init__(self):
		None

	async def printOnes(self):
		while True:
			print("printOnes from testClassOne running, printing every second")
			await asyncio.sleep(1)

class testClassTwo:
	def __init__(self):
		None

	async def printTwos(self):
		while True:
			print("printTwos from testClassTwo running, printing every 2 seconds")
			await asyncio.sleep(2)

class testMissionMode:
	def __init__(self):
		self.number = [0]

	async def run(self):
		tOne = testClassOne()
		tTwo = testClassTwo()
		tasks = [asyncio.create_task(tTwo.printTwos()),asyncio.create_task(tOne.printOnes()),asyncio.create_task(self.getNumber(self.number)),asyncio.create_task(self.setNumber(self.number))]
		await asyncio.sleep(10) #Function runs for 10 seconds
		try:
			for t in tasks:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("exception in canceling in testMissionMode.run()")
		return

	async def setNumber(self, num):
		while True:
			num[0] = random.randint(1,101)
			print("number set as " + str(num[0]))
			await asyncio.sleep(5)

	async def getNumber(self, num):
		while True:
			print("number read as " + str(num[0]))
			await asyncio.sleep(5)

