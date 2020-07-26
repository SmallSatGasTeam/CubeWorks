import io
import sys
# import Check - DOESN'T EXIST
import sqlite3
import struct
import subprocess
import calendar
import time

#we need import jacks camera code from the drivers
#we need import the boom deployer code from the drivers

### TODO: pass file location to Radio TX EXE
        ###import the camera driver
        ###import the boom driver
        ###import the command to tell the pi to turn off (watchdog)
        
        
### TODO: Write the Epoch time stamp (miliseconds) at the beginning of the transmission
### TODO: Pass Datatype to shawn's code 
### TODO: flag last tramission
        
'''
Processes:
    #1. Read Trasmission
    #2. Decode Transmission (from hex)
    #3. Produce rxData list from decoded TX
    #4. Determine the type of request recieved (database query or command)
    #5. Decide if transmitting DataType or Picture
    #6. Get packets or picture from the database
    #7. Packetize data and write to a file 
    #8. Wait until 5 seconds before the tx window starts
    #9. Call Shawn's Code
    #10. Exit (close interrupts if made)
'''

class TXISR:
    '''
    rxData holds the values gotten from the grounds transmission. (see Flight Logic doc appendix c table 5)
    0 = packet type
    1 = window start
    2 = window duration
    3 = data type
    4 = picture number (if applicable)
    '''
    rxData = ['#']
    outputFile = "test.txt"
    # commented for testing purposes
    # inputFile = "/dev/tty/AMA0"
    inputFile = "C:/Users/Get Away Special/Desktop/Build RX H/transTestAttitude.txt"
    
   
    def readTX(self):
        '''
        Process #1 & #3
        '''
        for i in range(5):
            currentData = self.TX.readline()
            currentData = self.decodeTX(currentData)
            self.rxData.append(currentData)
            
    def decodeTX(self, hexMessage):
        '''
        Process #2
        '''
        # USE THIS IN ACTUAL CODE:::
        # return bytes.fromhex(hexMessage).decode('utf-8')
        # testing RETURN VALUE FOR RECIEVING A STRING:
        return int(hexMessage, 0)

    def __init__(self):
         
        if not path.exists(self.inputFile):
            print("INPUT FILE NOT FOUND")
            sys.exit()
        else:
            self.TX = open(self.inputFile, 'r')
            self.readTX()    
        
        self.commandRecived()

    def sendTosrCheck(self):
        Check(self.rxData[3], self.rxData[1], self.rxData[2])
    
    def drivePic (self, dataType, picNum):
        '''
        function if a picture is desired
        '''
        data = []
        
        if dataType == 3:
            picRes = h
        elif dataType == 4:
            picRes = l
        else:
            exit(1)
        
        data = self.getPicture(picNum, picRes)

        numLines = self.packetize(True, data)

        # delay 5 seconds to the start of the transmission window, then call Radio Driver
        curTime = calendar.timegm(time.gmtime())
        delay = ((winStart - curTime) - 5)
        time.sleep(delay)
            
        self.callRadioDriver(numLines, dataType, winDur)
        
    def driveDataType (self, dataType):   
        '''
        function if no picture is requested 
        '''
        data = []
        #data = self.getPackets(sys.argv[1], sys.argv[3])
        
        ### TODO: Get packets from the files on the system
        data.reverse()
        
        numLines = self.packetize(False, data)
        
        # delay 5 seconds to the start of the transmission window, then call Radio Driver
        ## TODO: MOVE THIS THE THE INTURRUPT CODE:
        curTime = calendar.timegm(time.gmtime())
        delay = ((winStart - curTime) - 5)
        time.sleep(delay)
            
        self.callRadioDriver(numLines, dataType, winDur)
        

    def packetize(self, isPic, *dataList):
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
            self.wipeTxFile()
            
            f = open(self.outputFile, 'a')

            linesTotal = 0

            for tup in dataList:
                for value in tup:
                
                    ### STRING METHOD:
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
            f.write('@')
            f.write('\n')
        f.write(str(linesTotal))
        f.close()
        return linesTotal

    def wipeTxFile():
        file = open(self.outputFile,"r+")
        file.truncate(0)
        file.close()
        
    ### This part of the code checks to see if we are reciving a command to do something. 
    def commandReceived(self):
    '''
    Process #4
    '''
        if(self.rxData[0] == 0):
            ### TODO PROCESS ALL THE OPTIONS FOR THE DATA TYPES
            return
        else :
            #turn off tx
            if(self.rxData[1] == 0):
                canTX = False
            #take pic
            else if(self.rxData[2] == 1) :
                #photo.Camera()
            #deploy boom
            else if(self.rxData[3] == 1) :
                #boom.boomDeployer()
            else if(self.rxData[4] == 1) :
                #reboot pi, send command to adruino
            else :
                return
                

    def getCanTX(self):
        return self.canTX

'''
DEPRETIATED FUNCTIONS:

    
    def driveSql (self, packType, winStart, winDur, dataType, sqlStatement):
        # function if an arbitrary sql statement is requested
        data = []
        
        data = self.getArbitrary(sqlStatement)
        
        ### TODO: Determine how to packetize arbitrary sql statement 
        # numLines = packetize(True, data)
        #
        
        # delay 5 seconds to the start of the transmission window, then call Radio Driver
        curTime = calendar.timegm(time.gmtime())
        delay = ((winStart - curTime) - 5)
        time.sleep(delay)
            
        self.callRadioDriver(numLines, dataType, winDur)
        
    def getPackets(self, pacType, numPackets):
        """
        Constructs an sql query based on pacType and numPackets, returns the result.
        Process #6
        """
        lastTransmitted = 0
        connection = sqlite3.connect('../db.sqlite3')
        cursor = connection.execute(f'SELECT * FROM {pacType} WHERE time > {lastTransmitted} ORDER BY time DESC LIMIT {numPackets}')
        rows = cursor.fetchall()
        return rows            

    def getPicture(self, picNum, res):
        """
        ... Actually, I don't know what this should do yet...
        Process #6
        """
        pass

    def getArbitrary(self, query):
        """
        executes arbitrary sql on the database target, returns whatever comes out.
        """
        connection = sqlite3.connect('../db.sqlite3')
        cursor = connection.execute(query)
        rows = cursor.fetchall()
        return rows
    
    ### HEX METHOD FUNCITON:      
    def num_to_hex(n):
        return hex(struct.unpack('<I', struct.pack('<f', n))[0])

    ### USE THIS METHOD TO DECODE THE HEX STREAM (if being used) WHEN RECIEVED ON THE GROUND:
    def hex_to_num(h):
        h = str(h)
        h = h.replace("0x", "")
        return struct.unpack('!f', h.decode('hex'))[0]
'''