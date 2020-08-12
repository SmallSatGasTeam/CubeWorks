'''
This file will be used to process the packets that are received from the ground. Before the packets reach this file, they will be sent to the radio and then over UART to the pi.
The pythonInterrupt.py file monitors the UART buffer, and when data is received it will gather the data byte by byte and then parse the data for the header and footer that should be located on either end of our packets.
The header and footer is the Hex representation of 'GASPACS'. The pythonInterrupt.py takes the packet data located in between the header and footer and then calls the processPacket() method located in this file, passing in an argument containing the packet data.
processPacket() will convert the packet data to binary, and then go through bit by bit and perform the functionality specified in the packet.
'''
# NOTE: This code is not asyncronous currently.
import sys
sys.path.append('../')
import time
import os.path
import Drivers.camera.Camera as camera
import Drivers.boomDeployer as boomDeployer
import smbus

def processPacket(packetData):
	# Packet data comes in as hex, need to convet to binary to parse
	binaryDataLength = len(packetData) * 4
	binaryData = format(int(packetData,16), 'b').zfill(binaryDataLength)

	if binaryData[0] == '0':
		# This is a TX Schedule packet.
		print("TX Schedule Packet")
		
		# Get window start delta T
		windowStartBinary = binaryData[1:33]
		windowStartDecimal = int(windowStartBinary,2)
		print("Window start in seconds: ", windowStartDecimal)
		
		# Get window duration
		windowDurationBinary = binaryData[33:49]
		windowDurationDecimal = int(windowDurationBinary,2)
		print("Window duration in seconds: ", windowDurationDecimal)
		
		# Get data type
		dataTypeBinary = binaryData[49:57]
		dataTypeDecimal = int(dataTypeBinary,2)
		print("Data type: ", dataTypeDecimal)
		
		# Get picture number
		pictureNumberBinary = binaryData[57:73]
		pictureNumberDecimal = int(pictureNumberBinary,2)
		print("Picture number: ", pictureNumberDecimal)
		
		writeTXWindow(windowStartDecimal, windowDurationDecimal, dataTypeDecimal, pictureNumberDecimal)
	else:
		# This is a command packet
		print("Command packet")
		if binaryData[1] == '0':
			# Turn off Transmitter
			print("Turn off Transmissions")
			disableTransmissions()
		else:
			#Turn on Transmitter
			print("Turn on Transmitter")
			enableTransmissions()
			
		if binaryData[2] == '0':
			# DO NOT Clear TX Schedule and Progress
			print("Do NOT Clear TX Schedule and Progress")
		else:
			# Clear TX Schedule & Progress
			print("Clear TX Schedule and Progress")
			clearTXFile()
			clearTXProgress()
			
		if binaryData[3] == '0':
			# Do not take picture
			print("Do not take picture")
		else:
			# Take picture
			print("Take picture")
			cam = camera.Camera()
			cam.takePicture()
			
		if binaryData[4] == '0':
			# Do not deploy boom
			print("Do not deploy boom")
		else:
			# Deploy boom
			print("Deploy boom")
			deployer = boomDeployer.BoomDeployer()
			deployer.deploy()
			
		if binaryData[5] == '0':
			# Do not reboot
			print("Do not reboot")
		else:
			#Send reboot command to Beetle
			print("Reboot")
			###
			# TODO Kill the Heartbeat code
			###
			bus = smbus.SMBus(1)
			address = 0x08
			bus.write_byte(address, 1)
			
def writeTXWindow(windowStart, windowDuration, dataType, pictureNumber):
	# This function will write the TX window packet information to a file. Pass in the window start (delta T), window duration, data type, and picture number.
	# Note that this function saves the window start as an actual time, not a delta T - this is critical.

	# Convert window start from delta T to seconds since epoch
	windowStartTime = windowStart + int(time.time())
	print("Current time: ", int(time.time()))
	print("Start time: ", windowStartTime)
	
	TXWindow_File = open("/home/pi/Comms/CubeWorks/TXISR/data/txWindows.txt", "a+")
       
	#write the data to the file,
	TXWindow_File.write(str(windowStartTime)+',')
	TXWindow_File.write(str(windowDuration)+',')
	TXWindow_File.write(str(dataType)+',')
	TXWindow_File.write(str(pictureNumber))
	TXWindow_File.write('\n')
	
	# close file
	TXWindow_File.close()
	
def disableTransmissions():
	# This function will set a flag that will disable the radio transmissions. We will check the flag before making any transmissions.
	transmissionFlag_File = open("/home/pi/Comms/CubeWorks/TXISR/data/transmissionFlag.txt", "w")
	
	# write the data to the file,
	transmissionFlag_File.write("Disabled")
	
	# close the file
	transmissionFlag_File.close()
	
def enableTransmissions():
	# This function will set a flag that will disable the radio transmissions. We will check the flag before making any transmissions.
	transmissionFlag_File = open("/home/pi/Comms/CubeWorks/TXISR/data/transmissionFlag.txt", "w")
	
	# write the data to the file,
	transmissionFlag_File.write("Enabled")
	
	# close file
	transmissionFlag_File.close()
	
def clearTXFile():
	# This function clears the TX windows file
	transmissionFlag_File = open("/home/pi/Comms/CubeWorks/TXISR/data/txWindows.txt", "w")
	
	# close file
	transmissionFlag_File.close()
	
def clearTXProgress():
	# This function will clear the file that saves which timestamp has been transmitted most recently for each data type
	print("I don't know which file to clear!!!")
	
	
	
# Command packet
# processPacket('C8')
# TX Window Packet
#processPacket('0000000F007801000000')
