import asyncio
import sys
sys.path.append('../')
from TXISR import pythonInterrupt

asyncio.run(pythonInterrupt.interrupt())
