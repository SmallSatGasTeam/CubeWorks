import asyncio
import sys
import os
import time
sys.path.append('../')
from TXISR import pythonInterrupt
from TXISR import packetProcessing
from TXISR import prepareFiles
#This file duplicates the functionality of POST-BOOM deploy as it relates to communications

class testTransmissions():
	timeToNextWindow = 1
	nextWindowTime = -1
	duration = -1
	datatype = -1
	pictureNumber = -1

	TRANSFER_WINDOW_BUFFER_TIME = 10 #30 seconds
	REBOOT_WAIT_TIME = 900 #15 minutes, 900 seconds

	async def main(self):
		while True:
			txWindowsPath = '/home/pi/TXISRData/txWindows.txt'
			asyncio.create_task(pythonInterrupt.interrupt())
			asyncio.create_task(self.readNextTransferWindow(txWindowsPath))
			print("Initialized async processes")
			while True:
				#if close enough, prep files
				#wait until 5 seconds before, return True
				print("Just inside of while loop")
				if(self.timeToNextWindow != -1 and self.timeToNextWindow<14): #If next window is in 2 minutes or less
					print("Inside of first if statement")
					if(self.datatype < 3): #Attitude, TTNC, or Deployment data
						print("Inside of the if of the second if statement.")
						prepareFiles.prepareData(self.duration, self.datatype, 0, -1)
						print("Preparing data")
					else:
						print("Inside of else of second if statement")
						prepareFiles.preparePicture(self.duration, self.datatype, self.pictureNumber)
						print("Preparing Picture data")
					break
				await asyncio.sleep(5)
			windowTime = self.nextWindowTime
			while True:
				print("Made it to the second infinite loop.")
				if((windowTime-time.time()) <= 5):
					print("Calling TXServiceCode")
					txisrCodePath = 'sudo /home/pi/CubeWorks0/TXISR/TXServiceCode/./TXService.run'
					os.system(txisrCodePath + ' ' + str(self.datatype)) #Call TXISR Code
					self.timeToNextWindow = -1
					break
				await asyncio.sleep(0.1) #Check at 10Hz until the window time gap is less than 5 seconds

			
	async def readNextTransferWindow(self, transferWindowFilename):
		while True:
			#read the given transfer window file and extract the data for the soonest transfer window
			transferWindowFile = open(transferWindowFilename)
			sendData = 0
			soonestWindowTime = 0
			for line in transferWindowFile:
				#print("reading line: ")
				#print(line)
				data = line.split(",")
				#data[0] = time of next window, data[1] = duration of window, data[2] = datatype, data[3] = picture number
				if(float(data[0]) - time.time() > self.TRANSFER_WINDOW_BUFFER_TIME):  #if the transfer window is at BUFFER_TIME milliseconds in the future
					if(soonestWindowTime == 0 or float(data[0]) - time.time() < soonestWindowTime):
						soonestWindowTime = float(data[0]) - time.time()
						sendData = data
			if not(sendData == 0):
				#print("Found next transfer window: ")
				#print(sendData)
				self.timeToNextWindow = float(sendData[0]) - time.time()
				self.duration = int(sendData[1])
				self.datatype = int(sendData[2])
				self.pictureNumber = int(sendData[3])
				self.nextWindowTime = float(sendData[0])
				#print(timeToNextWindow)
				#print(duration)
				#print(datatype)
				#print(pictureNumber)
			await asyncio.sleep(3) #Checks transmission windows every 10 seconds
if __name__ == '__main__':
	testtx = testTransmissions()
	asyncio.run(testtx.main())

