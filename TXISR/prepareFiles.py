import sys
sys.path.append('../')
import os
from math import ceil

def prepareData(duration, dataType, pictureNumber = 0):
	if (type == 0): #Attitude Data
		f
	elif (type == 1): #TTNC Data
		f
	elif (type == 2): #Deploy Data
		f
	elif (type == 3): #HQ Picture Data
		f
	else: #LQ Picture Data
		f
		
	progressLineNumber = 0 #Line number in Shawn's flag file for the progress of this specific data type
	packetLength = 41 #Bytes
	packetTime = 120 + packetLength*8/9600 #Transmission time for 1 packet of size packetLength
	numPackets = ceil(duration*1000/packetTime) + 15 #For safety, 15 extra packets compared to the number that will likely be transmitted
	transmissionFilePath = os.path.join(os.path.dirname(__file__), 'txServiceCode/txFile.txt') #File path to txFile. This is where data will be stored
	dataFilePath = os.path.join()
	
	os.remove(transmissionFilePath) #Remove txFile
	txDataFile = open(transmissionFilePath, 'w+') #Create and open TX File
	txDataFile.write(duration*1000 + '\n') #Write first line to txData. Duration of window in milliseconds
	
	progressFilePath = os.path.join(os.path.dirname(__file__), 'txServiceCode/flagsFile.txt') #File Path to Shawn's flag file, which stores transmission progress
	progressFile = open(progressFilePath) #Opens progress file as read only
	progressList = progressFile.read().splitlines()
	transmissionProgress = progressList[progressLineNumber]
	
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

		
def preparePicture(duration, dataType, pictureNumber)
			
			
	
	
