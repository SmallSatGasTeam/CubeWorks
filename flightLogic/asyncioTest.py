import asyncio
import time
import random

async def main(): #Imitates main flight logic function, run in console with asyncio.run(main())
	tMode = testMissionMode() 
	await asyncio.create_task(tMode.run()) #This is how mission modes will need to be run, probably
	print("tMode.run() should be finished now. Waiting 5 seconds then exiting")
	await asyncio.sleep(5) #This is how sleep will be done in the main function
	return

class testClassOne: #imitates a data-getter
	def __init__(self):
		None

	async def printOnes(self):
		while True:
			print("printOnes from testClassOne running, printing every second")
			await asyncio.sleep(1)

class testClassTwo: #Another data-getter
	def __init__(self):
		None

	async def printTwos(self):
		while True:
			print("printTwos from testClassTwo running, printing every 2 seconds")
			await asyncio.sleep(2)

class testMissionMode: #imitates a mission mode
	def __init__(self):
		self.number = [0] #Have to use a list to pass information back from asynchronous methods, since integers/booleans are immutable

	async def run(self): #Run function of mission mode
		tOne = testClassOne()
		tTwo = testClassTwo()
		tasks = [asyncio.create_task(tTwo.printTwos()),asyncio.create_task(tOne.printOnes()),asyncio.create_task(self.getNumber(self.number)),asyncio.create_task(self.setNumber(self.number))] #This is how background tasks must be set up
		await asyncio.sleep(10) #Function runs for 10 seconds
		try: #Probably stop tasks in mission modes, do it like this
			for t in tasks:
				t.cancel()
		except asyncio.exceptions.CancelledException:
			print("exception in canceling in testMissionMode.run()")
		return

	async def setNumber(self, num): #These two methods imitate somethign like the battery checker reporting whether battery level is good for deployment
		while True:
			num[0] = random.randint(1,101)
			print("number set as " + str(num[0]))
			await asyncio.sleep(5)

	async def getNumber(self, num):
		while True:
			print("number read as " + str(num[0]))
			await asyncio.sleep(5)

