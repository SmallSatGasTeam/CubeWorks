import sys
sys.path.append('../')
import os
from math import ceil

def prepareAttitude(duration):
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
	
	
