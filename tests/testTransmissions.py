import asyncio
import sys
sys.path.append('../')
from TXISR import pythonInterrupt
from TXISR import packetProcessing
from TXISR import prepareFiles
#This file duplicates the functionality of POST-BOOM deploy as it relates to communications
timeToNextWindow = -1
nextWindowTime = -1
duration = -1
datatype = -1
pictureNumber = -1

if __name__ == '__main__':
	asycnio.run(main())

async def main():
	asyncio.create_task(pythonInterrupt.interrupt())
	asyncio.create_task(readNextTransferWindow())
	while True:
		#if close enough, prep files
		#wait until 5 seconds before, return True
		if(timeToNextWindow is not -1 and timeToNextWindow<60): #If next window is in 2 minutes or less
			if(datatype < 3): #Attitude, TTNC, or Deployment data
				prepareFiles.prepareData(duration, datatype)
			else:
				prepareFiles.preparePicture(duration, datatype, pictureNumber)
			break
		await asyncio.sleep(5)
	windowTime = nextWindowTime
	while True:
		if((windowTime-time.time()) <= 5):
			txisrCodePath = os.path.join(os.path.dirname(__file__), '../../TXISR/TXServiceCode/TXService.run')
			os.system(txisrCodePath + ' ' + str(datatype)) #Call TXISR Code
			return True
		await asyncio.sleep(0.1) #Check at 10Hz until the window time gap is less than 5 seconds

async def readNextTransferWindow(transferWindowFilename):
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
			if(float(data[0]) - time.time() > TRANSFER_WINDOW_BUFFER_TIME):  #if the transfer window is at BUFFER_TIME milliseconds in the future
				if(soonestWindowTime == 0 or float(data[0]) - time.time() < soonestWindowTime):
					soonestWindowTime = float(data[0]) - time.time()
					sendData = data
		if not(sendData == 0):
			#print("Found next transfer window: ")
			#print(sendData)
			timeToNextWindow = float(sendData[0]) - time.time()
			duration = int(sendData[1])
			datatype = int(sendData[2])
			pictureNumber = int(sendData[3])
			nextWindowTime = float(sendData[0])
			#print(timeToNextWindow)
			#print(duration)
			#print(datatype)
			#print(pictureNumber)
		await asyncio.sleep(10) #Checks transmission windows every 10 seconds