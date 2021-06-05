import sys
sys.path.append('../')
import os
from Drivers.camera import Camera
from math import ceil
from binascii import hexlify
from protectionProticol.fileProtection import FileReset
import linecache


fileChecker = FileReset()

"""
This file sets up 2 methods, prepareData and preparePicture. prepareData is used for Attitude Data, TTNC Data, and Deploy Data. preparePicture is used to prepare the HQ or LQ pictures
Both prepare functions reset /TXISR/TXServiceCode/txFile.txt, and write to it the duration of the transmission window.
Then, each line consists of a 10-letter string with the timestamp or index of the packet, folowed by ':' and then the hex content of the packet
"""
def prepareData(duration, dataType, startFrom):
	if (dataType == 0): #Attitude Data
		packetLength = 37 + 14 #Packet length in bytes plus the 7 GASPACS bytes on each end
		fileChecker.checkFile('/home/pi/flightLogicData/Attitude_Data.txt')
		dataFilePath = ('/home/pi/flightLogicData/Attitude_Data.txt') #Set data file path to respective file
		print("Attitude Data selected")
	elif (dataType == 1): #TTNC Data
		packetLength = 92 + 14 #Packet length in bytes plus the 7 GASPACS bytes on each end
		fileChecker.checkFile('/home/pi/flightLogicData/TTNC_Data.txt')
		dataFilePath = ('/home/pi/flightLogicData/TTNC_Data.txt') #Set data file path to respective file		
		print("TTNC Data selected")
	else: #Deploy Data
		packetLength = 25 + 14 #Packet length in bytes plus the 7 GASPACS bytes on each end
		fileChecker.checkFile('/home/pi/flightLogicData/Deploy_Data.txt')
		dataFilePath = ('/home/pi/flightLogicData/Deploy_Data.txt') #Set data file path to respective file		
		print("Deploy Data selected")
	minFileSize = packetLength*2+12 #Minimum characters in file

	packetTime = 120 + packetLength*8/9600 #Transmission time for 1 packet of size packetLength
	numPackets = ceil(duration*1000/packetTime) + 15 #For safety, 15 extra packets compared to the number that will likely be transmitted

	transmissionFilePath = ('../TXISR/data/txFile.txt') #File path to txFile. This is where data will be stored
	fileChecker.checkFile(transmissionFilePath)	
	txDataFile = open(transmissionFilePath, 'w') #Create and open TX File
	txDataFile.write(str(duration*1000) + '\n') #Write first line to txData. Duration of window in milliseconds

	print("Made it through transmission file path.")

	progressFilePath = ('/home/pi/TXISRData/flagsFile.txt') #File Path to Shawn's flag file, which stores transmission progress
	fileChecker.checkFile(transmissionFilePath)	
	progressFile = open(progressFilePath, 'r+') #Opens progress file as read only
	progressList = progressFile.read().splitlines()
	print("Made it through progress FilePath.")

	# Try reading transmission progress from file, if that fails (file is blank) set progress to 0 and write 5 lines of 0's
	try:
		transmissionProgress = int(progressList[dataType])
	except:
		transmissionProgress = 0
		print("Progress list didn't exist.")
		progressFile.write("0\n0\n0\n0\n0\n")

#NOTE: This is a new section of code to try and allow indexing in the file_____
	fileChecker.checkFile(dataFilePath)
	dataFile = open(dataFilePath, "r")
	print("data file size: ", os.stat(dataFilePath).st_size)
	print("min file size: ", minFileSize)
	if(os.stat(dataFilePath).st_size >= minFileSize): #File is of minimum length
		print("enough data")
		pass
	else:
		print("not enough data")
		return
	#This is where the new code starts_________________________________________
	dataFile.close()
	#If -1 is passed to StartFrom then search for the furthest transmitted data
	if startFrom == -1:
		print("Transmitting from last transmission")
		lineNumber = 0
		progressFile.seek(transmissionProgress)
		lineNumber = progressFile.tell()

		dataSize = 0
		while dataSize < numPackets:
			line = linecache.getline(dataFilePath, lineNumber)
			"""What's the purpose of this if statement? I can tell that it's
			checking to make sure that we don't hit the end of the file, but
			why does it go back to the beginning of the file? I'm guessing
			that it's just because we need to send the exact same size of packet
			and needed filler data. But why go back to the beginning? wouldn't
			it be better just to filler data so we knew exactly what to look
			for in extra data?"""
			if line == "":
				print("At the end of the file")
				lineNumber = 1
				#Why do we need continue if we're not skipping anything?
				continue
			else:
				print("In the middle of the file")
				txDataFile.write(line)
				dataSize += 1
				lineNumber += 1
				#Does this line need to be here? Woudln't it just do nothing? 
				continue
	else:
		print("Preparing file from line.", startFrom)
		dataSize = 0
		lineNumber = startFrom
	
		while dataSize < numPackets:
			if (line == "") | (lineNumber == 0):
				line = linecache.getline(dataFilePath, 1)
				txDataFile.write(line)
				dataSize+=1
				lineNumber = 2
			else:
				line = linecache.getline(dataFilePath, lineNumber)
				txDataFile.write(line)
				lineNumber+=1
				dataSize+=1

	progressFile.close()
	txDataFile.close()

def preparePicture(duration, dataType, pictureNumber, index):
	if dataType == 3: #HQ Picture
		cam = Camera()
		cam.compressHighResToFiles(pictureNumber)
		dataFilePath = '/home/pi/flightLogicData/Pictures/'+str(pictureNumber)+'/HighRes/HighResOriginal'+str(pictureNumber)+'.bin'
	else: #LQ picture
		cam = Camera()
		cam.compressLowResToFiles(pictureNumber)
		dataFilePath = '/home/pi/flightLogicData/Pictures/'+str(pictureNumber)+'/LowRes/LowResOriginal'+str(pictureNumber)+'.bin'

	numPackets = ceil(duration*1000/(120 + 128*8/9600)) + 15 #How many picture packets can we transmit in the window? + 15 for safety

	transmissionFilePath = ('../TXISR/data/txFile.txt') #File path to txFile. This is where data will be stored
	fileChecker.checkFile(transmissionFilePath)
	try:
		os.remove(transmissionFilePath) #Remove txFile
	except:
		pass #FileNotFoundError is thrown if file doesn't exist
	print('got here')
	fileChecker.checkFile(transmissionFilePath)
	txDataFile = open(transmissionFilePath, 'w+') #Create and open TX File
	txDataFile.write(str(duration*1000) + '\n') #Write first line to txData. Duration of window in milliseconds

	progressFilePath = ('/home/pi/TXISRData/flagsFile.txt') #File Path to Shawn's flag file, which stores transmission progress
	fileChecker.checkFile(progressFilePath)
	progressFile = open(progressFilePath) #Opens progress file as read only
	progressList = progressFile.read().splitlines()
	# If Start From Beginning flag is false, set transmissionProgress to the last transmitted packet. Else, set to true to start from beginning.
	if(index == -1):
		transmissionProgress = int(progressList[dataType])
	else:
		transmissionProgress = 0

	fileChecker.checkFile(dataFilePath)
	pictureFile = open(dataFilePath, 'rb')
	pictureContent = hexlify(pictureFile.read()) #Picture content is now a string with the hex data of the file in it
	dataSize = 0
	position = transmissionProgress*128

	while dataSize < numPackets: #NOTE: @SHAWN THIS WILL BREAK IF THE FILE IS LESS THAN 128 bytes
		substringOfData = pictureContent[position:position+128].decode()
		if(len(substringOfData)<128): #EOF - Loop back to start
			position = 128-len(substringOfData)
			substringOfData += pictureContent[0:position].decode()
		else: #Nominal situation
			position=position+128
		txDataFile.write(str(dataSize).zfill(10)+':'+substringOfData+'\n')
		dataSize+=1

	progressFile.close() #Close files
	pictureFile.close()
	txDataFile.close()
