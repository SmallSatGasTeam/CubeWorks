#Shawn's pre review notes:
# Time here is declared as an int, I would not do that beacuse it could overflow. Just let python handle it. 
# Also when this class gets called by flight logic it will pass it an object that will handle getting the data we have stored.
# Inturrupt requires Pin

# from machine import Pin
# from multiprocessing import Process
from datetime import datetime
import time
import calendar
import os
import string
import sys
import asycnio

#import rxHandling.py
import rxHandling

# Voltage comming through pin upon reception 
CONST_VOLTAGE = 1.5

# Code that runs 
TRANSMIT_EXE = "TXServiceCode/TXService.run"

# Code that scans the UART
READ_EXE = "TXServiceCode/watchUARTRX.run"
    
# file with tx windows and durations. Eachline should have <timestamp of start of tx window> <duration of window>
TX_WINDOWS_FILE = "data/TxWindows.txt"

if __name__ == 'main'():
   '''
   start two infinitely running functions
   '''
   watchTxWindows()
   watchReceptions()
   '''
   p1 = Process(target=watchTxWindows)
   p1.start()
   p2 = Process(target=inturruptWatchReceptions)
   p2.start()
   p1.join()
   p2.join()
   '''

'''
START PROCESS 1 (p1) DEFINITION 
'''
async def watchTxWindows():
    '''
    watch windows and call to transmit if within window.
    '''
    # get current time
    current_time = int(time.time())

    f = open(TX_WINDOWS_FILE, 'r')
    
    nextTimeFound = False 
    
    # Should be an infinite loop
    while nextTimeFound == False:
        line = fp.readline()
        line = line.replace('\n','')
        line = line.split(' ')
        if line[0] == '':
            print("no TX window is listed. FAILING...")
        if current_time < int(line[0]):
            delay = (int(line[0]) - int(current_time))
            if delay < 0:
                print("Something went bad, cannot have negative wait time")
            time.sleep(delay - 5)
        
            dataTypeWithSpace = " "+line[1]
            callRadioDriver(dataTypeWithSpace)
    f.close()  
    
 def callRadioDriver(dataType):
    '''
    Function that calls TX EXE
    '''
    # FNULL = open(os.devnull, 'w')
    os.system(TRANSMIT_EXE+dataType)
    
'''
END PROCESS 1 DEFINITION
'''

'''
START PROCESS 2 (p2) DEFINITION
'''
async def watchReceptions():
    checking = os.system(READ_EXE)

    while not checking:
        checking = os.system(READ_EXE)
        if checking:
            x = rxHandling.TXISR()

'''
END PROCESS 2 DEFINITION
'''

'''
Depricated Functions:


#this class handles the tx files
class txWindows
    def __init__(self, startTime)
        self.tx = open(txSchedual)
        self.startTime = startTime

    #this func will add the window to our tx file
    def creatTXSchedual(self, schedual):
        self.tx.append(schedual)

    def waitForTx(self):
        window = self.tx.readline
        while((self.startTime + time.time()) != window)
        {}
        
async def inturruptWatchReceptions():
    #TODO: get the correct pin for the radio connection. 1.5-1.8 voltage
    btn = Pin(0, Pin.IN)

    # Create inturrupt
    btn.irq(callRxHandeling(btn))
    

def callRxHandeling(btn):
    # If data comes across pins, call rxHandeling to process incomming data
    if btn.value() >= CONST_VOLTAGE
       x = rxHandling.TXISR()

'''
