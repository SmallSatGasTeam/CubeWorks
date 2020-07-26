# Inturrupt requires Pin
from machine import Pin
from multiprocessing import Process
from datetime import datetime
import time
import calendar

#import rxHandling.py
import rxHandling

voltage = 1.5

def watchReceptions(btn):
    ## I think this is how this works...
    if btn.value() >= voltage
       x = rxHandling.TXISR()

def watchTxWindows():
    #get current time
    current_time = int(time.time())
    
    filePath = "C:/Users/dstevens/Documents/GitHub/CubeWorks/TXISR/testFiles/TxWindows.txt"
    f = open(filePath, 'r')
    
    nextTimeFound = False 
    
    # Should be an infinite loop
    while nextTimeFound == False:
        line = fp.readline()
        line = line.replace('\n','')
        if line == '':
            print("no TX window is listed. FAILING...")
        if current_time < int(line):
            delay = (int(line) - int(current_time))
            if delay < 0:
                print("Something went bad, cannot have negative wait time")
            time.sleep(delay - 5)
            
            # TODO: ADD winDur
            #winDur = <SOMETHING>
            callRadioDriver(winDur)
    
    f.close()
    
    
 def callRadioDriver (txWindow):
    '''
    Function that calls TX EXE
    '''

    FNULL = open(os.devnull, 'w')
    args = TxExe "-<ARGUMENTS>"
    subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)
    #subprocess.call(["<PATH_TO_TX_EXE>"])
    #subprocess.run(["<PATH_TO_FILE>", "-arg1 numRecords", "-dt dataType", "-tw txWindow"])   

def inturruptWatchReceptions():
    # Part of inturrupt method 1:
    #TODO: get the correct pin for the radio connection. 1.5-1.8 voltage
    btn = Pin(0, Pin.IN)

    # Create inturrupt
    btn.irq(watchReceptions(btn))
    # TODO: watch tx windows, if we hit one, call Shawn's code


if __name__ == 'main'():
   p1 = Process(target=inturruptWatchReceptions)
   p1.start()
   p2 = Process(target=watchTxWindows)
   p2.start()
   p1.join()
   p2.join()


'''
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