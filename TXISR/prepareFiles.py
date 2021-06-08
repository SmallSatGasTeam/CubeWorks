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
	#If -1 is passed to StartFrom then search for the furthest transmitted data
	if startFrom == -1:
		print("Starting from last transmitted line.")
		lineNumber = 0
		for index, line in enumerate(dataFile):
			print("Index:", index, "Line:", int(line[1:10]), "Searching for:", transmissionProgress)
			if int(line[1:10]) == transmissionProgress:
				print("Found the correct line")
				lineNumber = int(index) + 1
				break
		print("The lineNumber found is", lineNumber)
		dataFile.close()

		dataSize = 0
		while dataSize < numPackets:
			line = linecache.getline(dataFilePath, lineNumber)
			if (line == "") | (lineNumber == 0):
				print("End of the line, resetting.")
				lineNumber = 1
				continue
			else:
				txDataFile.write(line)
				dataSize += 1
				lineNumber += 1
				#Does this line need to be here? Woudln't it just do nothing? 
				continue
	else:
		dataSize = 0
		lineNumber = startFrom
		print("Starting from the provided line:", lineNumber)
	
		while dataSize < numPackets:
			line = linecache.getline(dataFilePath, lineNumber)
			if (line == "") | (lineNumber == 0):
				print("At the end of the file, going back to the beginning")
				lineNumber = 1
				continue
			else:
				txDataFile.write(line)
				lineNumber+=1
				dataSize+=1

	print("Finished prepare files.")
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

	print("Line 141")

	progressFilePath = ('/home/pi/TXISRData/flagsFile.txt') #File Path to Shawn's flag file, which stores transmission progress
	fileChecker.checkFile(progressFilePath)
	progressFile = open(progressFilePath) #Opens progress file as read only
	progressList = progressFile.read().splitlines()
	# If Start From Beginning flag is false, set transmissionProgress to the last transmitted packet. Else, set to true to start from beginning.
	if(index == -1):
		transmissionProgress = int(progressList[dataType])
	else:
		transmissionProgress = 0

	print("Line 153")

	try:
		fileChecker.checkFile(dataFilePath)
		pictureFile = open(dataFilePath, 'rb')
		pictureContent = hexlify(pictureFile.read()) #Picture content is now a string with the hex data of the file in it
		dataSize = 0
		print("Transmission progress is:", transmissionProgress)
		position = transmissionProgress*128
		print("Position is:", position)
		gaspacsHex = str(b'GASPACS'.hex())
		pictureContent += gaspacsHex
	except Exception as e:
		print("Error: " + e)

	print("Line 165")

	while dataSize < numPackets: #NOTE: @SHAWN THIS WILL BREAK IF THE FILE IS LESS THAN 128 bytes
		substringOfData = pictureContent[position:position+128].decode()
		if(len(substringOfData)<128): #EOF - Loop back to start
			position = 128-len(substringOfData)
			substringOfData += pictureContent[0:position].decode()
		else: #Nominal situation
			position=position+128
		txDataFile.write(str(transmissionProgress).zfill(10)+':'+substringOfData+'\n')
		dataSize+=1
		transmissionProgress += 1

	print("Finished prepare files.")
	progressFile.close() #Close files
	pictureFile.close()
	txDataFile.close()