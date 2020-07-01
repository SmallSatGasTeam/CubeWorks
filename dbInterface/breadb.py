import sys
import sqlite3
import struct
import subprocess
import calendar
import time

### TODO: pass file location to Radio TX EXE
NombreDelArchivo = "test.txt"

def driver (packType, winStart, winDur, dataType, picNum):
    '''
    Overloaded function if a picture is desired
    '''
    data = []
    
    if dataType == 3:
        picRes = h
    elif dataType == 4:
        picRes = l
    else:
        exit(1)
    
    data = getPicture(picNum, picRes)

    numLines = packetize(True, data)

    # delay 5 seconds to the start of the transmission window, then call Radio Driver
    curTime = calendar.timegm(time.gmtime())
    delay = ((winStart - curTime) - 5)
    time.sleep(delay)
        
    callRadioDriver(numLines, dataType, winDur)
    
    
def driver (packType, winStart, winDur, dataType, sqlStatement):
    '''
    Overloaded function if an arbitrary sql statement is requested
    '''
    data = []
    
    data = getArbitrary(sqlStatement)
    
    ### TODO: Determine how to packetize arbitrary sql statement 
    # numLines = packetize(True, data)
    #
    
    # delay 5 seconds to the start of the transmission window, then call Radio Driver
    curTime = calendar.timegm(time.gmtime())
    delay = ((winStart - curTime) - 5)
    time.sleep(delay)
        
    callRadioDriver(numLines, dataType, winDur)
    
def driver (packType, winStart, winDur, dataType):   
    '''
    Overloaded function if no picture is requested 
    '''
    data = []
    data = getPackets(sys.argv[1], sys.argv[3])
    data.reverse()
    
    numLines = packetize(False, data)
    
    # delay 5 seconds to the start of the transmission window, then call Radio Driver
    curTime = calendar.timegm(time.gmtime())
    delay = ((winStart - curTime) - 5)
    time.sleep(delay)
        
    callRadioDriver(numLines, dataType, winDur)
    
def callRadioDriver (numRecords, dataType, txWindow):
    '''
    Function that calls TX EXE
    '''
    ### TODO: TEST SUBPROCESS CALL METHOD ON EXE

    FNULL = open(os.devnull, 'w')
    args = "<PATH_TO_FILE> -<ARGUMENTS>"
    subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)
    #subprocess.call(["<PATH_TO_TX_EXE>"])
    #subprocess.run(["<PATH_TO_FILE>", "-arg1 numRecords", "-dt dataType", "-tw txWindow"])

def packetize(isPic, *dataList):
    """
    Takes an list(tuple(data)) from the database and writes a binary stream to a file
    call packetize(*<LIST NAME>, <BOOL VARIABLE>)
    """
    
    linesTotal = 0
    
    if isPic == True:
        ### TODO: Decide how to packetize a picture
        ### TODO: Locate the picture data and report to TX function .exe
        pass
    elif isPic == False:
        wipeTxFile()
        
        f = open(NombreDelArchivo, 'a')

        linesTotal = 0

        for tup in dataList:
            for value in tup:
            
                ### TODO: STRING METHOD:
                f.write(str(value))
                f.write(',')
                 
                ## BINARY METHOD
                #ba = bytearray(struct.pack("f", value))
                #t = ""
                #for b in ba:
                #    t = "0x%02x" % b
                
                ### HEX NUMBER METHOD: 
                #hexNum = num_to_hex(value)			   
                #f.write(hexNum)

                ### HEX STRING METHOD:
                #
                #
            
            f.write('\n')
            linesTotal += 1
        f.write(';')
        f.write('\n')
    f.write(str(linesTotal))
    f.close()
    return linesTotal

def wipeTxFile():
    file = open(NombreDelArchivo,"r+")
    file.truncate(0)
    file.close()
    
### HEX METHOD FUNCITON:
'''
def num_to_hex(n):
    return hex(struct.unpack('<I', struct.pack('<f', n))[0])
'''
### USE THIS METHOD TO DECODE THE HEX STREAM (if being used) WHEN RECIEVED ON THE GROUND:
'''
def hex_to_num(h):
    h = str(h)
    h = h.replace("0x", "")
    return struct.unpack('!f', h.decode('hex'))[0]
'''

def getPackets(pacType, numPackets):
    """
    Constructs an sql query based on pacType and numPackets, returns the result.
    """
    lastTransmitted = 0
    connection = sqlite3.connect('../db.sqlite3')
    cursor = connection.execute(f'SELECT * FROM {pacType} WHERE time > {lastTransmitted} ORDER BY time DESC LIMIT {numPackets}')
    rows = cursor.fetchall()
    return rows
    

def getPicture(picNum, res):
    """
    ... Actually, I don't know what this should do yet...
    """
    pass

def getArbitrary(query):
    """
    executes arbitrary sql on the database target, returns whatever comes out.
    """
    connection = sqlite3.connect('../db.sqlite3')
    cursor = connection.execute(query)
    rows = cursor.fetchall()
    return rows


if __name__ == '__main__':
    """
    Usage: command [-flag optional] [options]
    no flag: [<packet_type> <tx_window> <number_of_packets>]
    -a: [<sql_statement>]
    -p: [<picture_number> <resolution>]

    flags: -a, execute arbitrary sql.  Must be followed by a valid sqlite statement.
           -p, get picture.  <picture_number> is a non-negative integer, <resolution> is the size of the picture to prepare.
    """

    ### TESTING RESOURCE:
    '''
    data = []
    if sys.argv[1] == '-a':
        data = getArbitrary(sys.argv[2])
    elif sys.argv[1] == '-p':
        data = getPicture(sys.argv[2], sys.argv[3])
    else:
        data = getPackets(sys.argv[1], sys.argv[3])
        data.reverse()
    print(data)
    '''
