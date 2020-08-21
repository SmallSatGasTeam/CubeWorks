import sys
import os
import asyncio
sys.path.append('../')
from flightLogic import mainFlightLogic

def recordData(bootCount, antennaDeployed, lastMode):
	#write to the boot file, "w" option in write overwrites the file
	new = open(os.path.dirname(__file__) + "../flightLogic../bootRecords", "w+")
	new.write(str(bootCount) + '\n')
	if antennaDeployed:
		new.write(str(1)+'\n')
	else:
		new.write(str(0)+'\n')
	new.write(str(lastMode) + '\n')
	new.close()

	# write to the the back up file
	new = open(os.path.dirname(__file__) + "/backupBootRecords", "w+")
	new.write(str(bootCount) + '\n')
	if antennaDeployed:
		new.write(str(1)+'\n')
	else:
		new.write(str(0)+'\n')
	new.write(str(lastMode) + '\n')
	new.close()


if __name__ == '__main__':
	argument = sys.argv[1]
	if argument == '0':
		#BOOT mode
		recordData(0, False, 0)
		asyncio.run(mainFlightLogic.executeFlightLogic())
	elif argument == '1':
		#Antenna Deploy mode
		recordData(1, False, 1)
		asyncio.run(mainFlightLogic.executeFlightLogic())
	elif argument == '2':
		#Pre-boom deploy 
		recordData(2, True, 2)
		asyncio.run(mainFlightLogic.executeFlightLogic())
	elif argument == '3':
		#Boom deploy
		recordData(3, True, 3)
		asyncio.run(mainFlightLogic.executeFlightLogic())
	else:
		#Post-Boom deploy
		recordData(4, True, 4)
		asyncio.run(mainFlightLogic.executeFlightLogic())
