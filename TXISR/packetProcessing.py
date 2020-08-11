'''
This file will be used to process the packets that are received from the ground. Before the packets reach this file, they will be sent to the radio and then over UART to the pi.
The pythonInterrupt.py file monitors the UART buffer, and when data is received it will gather the data byte by byte and then parse the data for the header and footer that should be located on either end of our packets.
The header and footer is the Hex representation of 'GASPACS'. The pythonInterrupt.py takes the packet data located in between the header and footer and then calls the processPacket() method located in this file, passing in an argument containing the packet data.
processPacket() will convert the packet data to binary, and then go through bit by bit and perform the functionality specified in the packet.
'''
# NOTE: This code is not asyncronous currently.
def processPacket(packetData):
	# Packet data comes in as hex, need to convet to binary to parse
	binaryDataLength = len(packetData) * 4
	binaryData = format(int(packetData,16), 'b').zfill(binaryDataLength)
	print(binaryData)
	if binaryData[0] == '0':
		# This is a TX Schedule packet. The window start, duration, data type, and picture number are decimal format encoded in hex.
		print("TX Schedule Packet")
		windowStart = binaryData[1:34]
		print(WindowStart)
	else:
		# This is a command packet
		print("Command packet")
		if binaryData[1] == '0':
			# Turn off Transmitter
			print("Turn off Transmitter")
		else:
			#Turn on Transmitter
			print("Turn on Transmitter")
			
		if binaryData[2] == '0':
			# DO NOT Clear TX Schedule and Progress
			print("Do NOT Clear TX Schedule and Progress")
		else:
			# Clear TX Schedule
			print("Clear TX Schedule and Progress")
			
		if binaryData[3] == '0':
			# Do not take picture
			print("Do not take picture")
		else:
			# Take picture
			print("Take picture")
			
		if binaryData[4] == '0':
			# Do not deploy boom
			print("Do not deploy boom")
		else:
			# Deploy boom
			print("Deploy boom")
			
		if binaryData[5] == '0':
			# Do not reboot
			print("Do not reboot")
		else:
			#Send reboot command to Beetle
			print("Reboot")
			
# Command packet
# processPacket('C8')
# TX Window Packet
processPacket('0000000F007801000000')
