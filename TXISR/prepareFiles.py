import sys
sys.path.append('../')
import os
from math import ceil
from binascii import hexlify

def prepareData(duration, dataType, pictureNumber = 0):
	if (dataType == 0): #Attitude Data
		packetLength = 51 #Packet length in bytes
		dataFilePath = os.path.join(os.path.dirname(__file__), '../flightLogic/Attitude_Data.txt') #Set data file path to respective file
	elif (dataType == 1): #TTNC Data
		packetLength = 118 #Packet length in bytes
		dataFilePath = os.path.join(os.path.dirname(__file__), '../flightLogic/TTNC_Data.txt') #Set data file path to respective file
	else: #Deploy Data
		packetLength = 36 #Packet length in bytes
		dataFilePath = os.path.join(os.path.dirname(__file__), '../flightLogic/Deploy_Data.txt') #Set data file path to respective file

		
	packetLength = 41 #Bytes
	packetTime = 120 + packetLength*8/9600 #Transmission time for 1 packet of size packetLength
	numPackets = ceil(duration*1000/packetTime) + 15 #For safety, 15 extra packets compared to the number that will likely be transmitted
	
	transmissionFilePath = os.path.join(os.path.dirname(__file__), 'TXServiceCode/txFile.txt') #File path to txFile. This is where data will be stored
	try:
		os.remove(transmissionFilePath) #Remove txFile
	except:
		pass #FileNotFoundError is thrown if file doesn't exist
	
	txDataFile = open(transmissionFilePath, 'w+') #Create and open TX File
	txDataFile.write(str(duration*1000) + '\n') #Write first line to txData. Duration of window in milliseconds
	
	progressFilePath = os.path.join(os.path.dirname(__file__), 'TXServiceCode/flagsFile.txt') #File Path to Shawn's flag file, which stores transmission progress
	progressFile = open(progressFilePath) #Opens progress file as read only
	progressList = progressFile.read().splitlines()
	transmissionProgress = int(progressList[dataType])
	
	dataFile = open(dataFilePath) #Open data file, this gets copied into txFile.
	#NOTE: THIS COULD CAUSE ERRORS WITH THE FILE SIMULTANEOUSLY BEING WRITTEN INTO. THIS IS #1 ON LIST OF THINGS TO FIX POST-CDR!!! @SHAWN
	lineNumber = 0 #Line to start adding data from
	while True:
		line = dataFile.readline()
		if(int(line[:10])>transmissionProgress): #This line is further ahead than the transmission progress, transmit going from this line forwards.
			break
			
		if(line==''): #End of file without finding a line further than transmission progress
			lineNumber = 0
			break
			
		lineNumber += 1 #Advance by one line
	
	dataFile.seek(0) #Reset progress in file and go to the right line. This is an inefficient way of doing this, but it *will* work
	i=0
	while i<lineNumber:
		dataFile.readline()
		i+=1
	
	#Now, we are at the appropriate place in the file again. Start reading lines into transmission file
	dataSize = 0 #How many lines have we written to Data file?
	while dataSize<numPackets:
		line = dataFile.readline()
		if line == '': #End of file, seek to start
			dataFile.seek(0)
			continue
		else:
			txDataFile.write(line) #Write line from recorded data file into transmission file
			dataSize+=1
			continue

		
def preparePicture(duration, dataType, pictureNumber):
	if dataType == 3: #HQ Picture
		dataFilePath = os.path.join(os.path.dirname(__file__), '../../../Pictures/'+str(pictureNumber)+'/HighRes/HighResOriginal'+str(pictureNumber)+'.jpg') #TODO FIX!
	else: #LQ picture
		dataFilePath = os.path.join(os.path.dirname(__file__), '../../../Pictures/'+str(pictureNumber)+'/LowRes/LowResOriginal'+str(pictureNumber)+'.jpg')
	
	numPackets = ceil(duration*1000/(120 + 128*8/9600)) + 15 #How many picture packets can we transmit in the window? + 15 for safety
	
	transmissionFilePath = os.path.join(os.path.dirname(__file__), 'TXServiceCode/txFile.txt') #File path to txFile. This is where data will be stored
	try:
		os.remove(transmissionFilePath) #Remove txFile
	except:
		pass #FileNotFoundError is thrown if file doesn't exist
	
	txDataFile = open(transmissionFilePath, 'w+') #Create and open TX File
	txDataFile.write(str(duration*1000) + '\n') #Write first line to txData. Duration of window in milliseconds
	
	progressFilePath = os.path.join(os.path.dirname(__file__), 'TXServiceCode/flagsFile.txt') #File Path to Shawn's flag file, which stores transmission progress
	progressFile = open(progressFilePath) #Opens progress file as read only
	progressList = progressFile.read().splitlines()
	transmissionProgress = int(progressList[dataType])
	
	pictureFile = open(dataFilePath, 'rb')
	pictureContent = hexlify(pictureFile.read()) #Picture content is now a string with the hex data of the file in it
	dataSize = 0
	position = transmissionProgress*256
	
	while dataSize < numPackets: #NOTE: @SHAWN THIS WILL BREAK IF THE FILE IS LESS THAN 128 bytes
		substringOfData = pictureContent[position:position+256].decode()
		if(len(substringOfData)<256): #EOF - 
			position = 256-len(substringOfData)
			substringOfData += pictureContent[0:position]
		else: #Nominal situation
			position=position+256
		txDataFile.write(str(dataSize).zfill(10)+':'+substringOfData+'\n')
		dataSize+=1

	progressFile.close() #Close files
	pictureFile.close()
	txDataFile.close()
			
	
		
			
	
	
