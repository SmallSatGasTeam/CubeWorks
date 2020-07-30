# Inturrupt requires Pin
from machine import Pin
from multiprocessing import Process
from datetime import datetime
import time
import calendar

#import rxHandling.py
import rxHandling

# Voltage comming through pin upon reception 
CONST_VOLTAGE = 1.5

# Code that runs 
TRASMIT_EXE = "TXService.run"
    
# file with tx windows and durations. Eachline should have <timestamp of start of tx window> <duration of window>
TX_WINDOWS_FILE = "TxWindows.txt"

if __name__ == 'main'():
   '''
   start two infinitely running functions
   '''
   
   p1 = Process(target=watchTxWindows)
   p1.start()
   p2 = Process(target=inturruptWatchReceptions)
   p2.start()
   p1.join()
   p2.join()


'''
START PROCESS 1 (p1) DEFINITION 
'''
def watchTxWindows():
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
        
            callRadioDriver(line[1])
    f.close()  
    
 def callRadioDriver (txWindow):
    '''
    Function that calls TX EXE
    '''

    FNULL = open(os.devnull, 'w')
    args = TRASMIT_EXE "-<ARGUMENTS>"
    subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)
    #subprocess.call(["<PATH_TO_TX_EXE>"])
    #subprocess.run(["<PATH_TO_FILE>", "-arg1 numRecords", "-dt dataType", "-tw txWindow"])   
    
'''
END PROCESS 1 DEFINITION
'''

'''
START PROCESS 2 (p2) DEFINITION
'''
def inturruptWatchReceptions():
    #TODO: get the correct pin for the radio connection. 1.5-1.8 voltage
    btn = Pin(0, Pin.IN)

    # Create inturrupt
    btn.irq(callRxHandeling(btn))

def callRxHandeling(btn):
    # If data comes across pins, call rxHandeling to process incomming data
    if btn.value() >= CONST_VOLTAGE
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
'''