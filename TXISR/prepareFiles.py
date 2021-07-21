import sys
sys.path.append('../')
import os
from Drivers.camera import Camera
from math import ceil
from binascii import hexlify
from protectionProticol.fileProtection import FileReset
import linecache


fileChecker = FileReset()

# This file sets up 2 methods, prepareData and preparePicture. prepareData is used for Attitude Data, TTNC Data, and Deploy Data. preparePicture is used to prepare the HQ or LQ pictures
# Both prepare functions reset /TXISR/TXServiceCode/txFile.txt, and write to it the duration of the transmission window.
# Then, each line consists of a 10-letter string with the timestamp or index of the packet, folowed by ':' and then the hex content of the packet

#NOTE: each function trys to prepare the data, if it is successful it returns true, other wise it returns false
def prepareData(duration, dataType, startFrom):
	try :
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

		packetTime = 120  #Transmission time for 1 packet of size packetLength
		numPackets = ceil(duration*1000/packetTime) + 15 #For safety, 15 extra packets compared to the number that will likely be transmitted

		transmissionFilePath = ('../TXISR/data/txFile.txt') #File path to txFile. This is where data will be stored
		fileChecker.checkFile(transmissionFilePath)	
		txDataFile = open(transmissionFilePath, 'w') #Create and open TX File
		txDataFile.write(str(duration*1000) + '\n') #Write first line to txData. Duration of window in milliseconds

		print("Made it through transmission file path.")

		progressFilePath = ('/home/pi/TXISRData/flagsFile.txt') #File Path to Shawn's flag file, which stores transmission progress
		fileChecker.checkFile(transmissionFilePath)	
		fileChecker.checkFile(progressFilePath)
		progressFile = open(progressFilePath, 'r+') #Opens progress file as read only
		progressList = progressFile.read().splitlines()
		print("Made it through progress FilePath.")

		# Try reading transmission progress from file, if that fails (file is blank) set progress to 0 and write 5 lines of 0's
		try:
			transmissionProgress = int(progressList[dataType])
			print("transmissionProgress: ", str(transmissionProgress))
		except:
			transmissionProgress = 0
			print("Progress list didn't exist.")
			fileChecker.individualReset(progressFilePath)

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
			return False
		#This is where the new code starts_________________________________________
		#If -1 is passed to StartFrom then search for the furthest transmitted data
		startFrom -= 1
		print("Start: ", str(startFrom))
		if (startFrom == -1) and (transmissionProgress != 0):
			lineNumber = transmissionProgress + 1
			print("line number:", lineNumber)
			dataSize = 0
		else:
			dataSize = 0
			lineNumber = startFrom
			print("Starting from the provided line:", str(lineNumber))

		while dataSize < numPackets:
				line =  str(lineNumber) + ":" + linecache.getline(dataFilePath, lineNumber)
				if (line == (str(lineNumber) + ":" + '')) or (lineNumber == 0):
					#print("End of the line, resetting.")
					lineNumber = 1
					continue
				else:
					try :
						print(line)
						txDataFile.write(line)
						dataSize += 1
						lineNumber += 1
					except : 
						dataSize += 1
						lineNumber += 1
					#Does this line need to be here? Woudln't it just do nothing? 
					continue

		progressFile.close()
		txDataFile.close()
		return True
	except :
		print("Failed to prepare flight data")
		return False

# this function prepares the pictures, NOTE: it compresses the picture file each time it runs
def preparePicture(duration, dataType, pictureNumber, index, camObj):
	try :
		if dataType == 3: #HQ Picture
			cam = camObj
			cam.compressHighResToFiles(pictureNumber)
			try:
				dataFilePath = '/home/pi/flightLogicData/Pictures/'+str(pictureNumber)+'/HighRes/HighResOriginal'+str(pictureNumber)+'.bin'
			except:
				print("Bad picture number")
				return False
		else: #LQ picture
			cam = camObj
			cam.compressLowResToFiles(pictureNumber)
			dataFilePath = '/home/pi/flightLogicData/Pictures/'+str(pictureNumber)+'/LowRes/LowResOriginal'+str(pictureNumber)+'.bin'

		numPackets = ceil(duration*1000/120) + 15 #How many picture packets can we transmit in the window? + 15 for safety

		transmissionFilePath = ('../TXISR/data/txFile.txt') #File path to txFile. This is where data will be stored
		fileChecker.checkFile(transmissionFilePath)
		try:
			os.remove(transmissionFilePath) #Remove txFile
		except:
			pass #FileNotFoundError is thrown if file doesn't exist
		print("Opening the transmission file")
		fileChecker.checkFile(transmissionFilePath)
		txDataFile = open(transmissionFilePath, 'w+') #Create and open TX File
		txDataFile.write(str(duration*1000) + '\n') #Write first line to txData. Duration of window in milliseconds

		print("Opening the flags file")
		progressFilePath = ('/home/pi/TXISRData/flagsFile.txt') #File Path to Shawn's flag file, which stores transmission progress
		fileChecker.checkFile(progressFilePath)
		progressFile = open(progressFilePath) #Opens progress file as read only
		try:
			progressList = progressFile.read().splitlines()	
		except:
			print("Failed to read the flags file")
			fileChecker.individualReset(progressFilePath)
			progressList = progressFile.read().splitlines()
		# If Start From Beginning flag is false, set transmissionProgress to the last transmitted packet. Else, set to true to start from beginning.
		if(index == -1):
			try:
				transmissionProgress = int(progressList[dataType])
			except:
				transmissionProgress = 0
				# reset the flags file
				fileChecker.individualReset(progressFilePath)
		elif (index == 1):
			#It seemed to work best this way instead of putting 0 - Alex
			transmissionProgress = int(index-1)
		else:
			transmissionProgress = int(index)

		fileChecker.checkFile(dataFilePath)
		pictureFile = open(dataFilePath, 'rb')
		pictureContent = hexlify(pictureFile.read()) #Picture content is now a string with the hex data of the file in it
		dataSize = 0
		print("Transmission progress is:", transmissionProgress)
		position = transmissionProgress*256
		print("Position is:", position)

		while dataSize < numPackets: #NOTE: @SHAWN THIS WILL BREAK IF THE FILE IS LESS THAN 128 bytes
			substringOfData = pictureContent[position:position+256].decode()
			if(len(substringOfData)<256): #EOF - Loop back to start
				position = 256-len(substringOfData)
				substringOfData += pictureContent[0:position].decode()
			else: #Nominal situation
				position=position+256
			txDataFile.write(str(transmissionProgress).zfill(10)+':'+substringOfData+'\n')
			dataSize+=1
			transmissionProgress += 1

		progressFile.close() #Close files
		pictureFile.close()
		txDataFile.close()
		return True
	except :
		print("!!!Failed to Prepare picture data!!!")
		return False
