import asyncio
import sys
sys.path.append('../')
from TXISR import pythonInterrupt
from TXISR import packetProcessing
from TXISR import prepareFiles
#This file duplicates the functionality of POST-BOOM deploy as it relates to communications

if __name__ = '__main__':
	asyncio.create_task(pythonInterrupt.interrupt())
	asyncio.create_task(readNextTransferWindow())
	asyncio.create_task(rebootLoop())
