import io
import sys
import struct
import subprocess
import calendar
import time
import serial

class TXISR:
    
    # List that stores eveything recieved in the transmission
    rxData = ['#']
    
    dataList = [['#']]
    
    # Define location of file where the data will be placed while waiting transmission
    outputFile = "TXServiceCode/txFile.txt"
    
    #define location where we will put the flags (flags are the last time each datatype trasmitted)
    flagsFile = "TXServiceCodde/flagsFile.txt"
    
    # Datatype Files
    attitudeDataFile = "data/attitudeData.txt"
    TTCDataFile = "data/ttcData.txt"
    deployDataFile = "data/deployData.txt"
    HQPicFile = "data/hpPicData.txt"
    LQPicFile = "data/lqPicData.txt"
    
    # TX Window Files
    TxWindows = "data/TxWindows.txt"
    
    # Define file where transmission will be recieved
    # commented out for testing purposes:
    UART_PORT = "/dev/ttyAMA0"
    # file for testing purposes:
    #inputFile = "data/AMA0_TEST.txt"

    # Bytes being recieved over UART, this gets changed in the parameterized constructor
    UART_BYTES = 0
    
    def __init__(self, bytes):
        '''
        Constructor. This will drive the process.
        '''
        self.UART_BYTES = bytes

        if not path.exists(self.inputFile):
            print("INPUT FILE NOT FOUND")
            sys.exit()
        else:
            SER = serial.Serial(UART_PORT)
            SER.baudrate = 115200
            inputString = SER.read(UART_BYTES)
            self.readTX(inputString)
            
        # commandRecieved will figure out how to process based on the command received
        self.commandReceived()

    
    def readTX(self, inputString):
        '''
        Read-in and decode transmission. Place decoded transmission in rxData
        '''
        for i in range(0, len(inputString)):
            currentData = inputString[i]
            currentData = bytes.fromhex(currentData).decode('utf-8')
            self.rxData.append(currentData)
    
    def commandReceived(self):
        '''
        Decide what to do based on the command recieved
        '''
        if(self.rxData[0] == 0):
            ### TODO PROCESS ALL THE OPTIONS FOR THE DATA TYPES
            if(self.rxData[3] == 0):
                # Process Attitude Data
                driveDataType(self.attitudeDataFile)
            elif(self.rxData[3] == 1):
                # Process TT&C Data
                driveDataType(self.TTCDataFile)
            elif(self.rxData[3] == 2):
                # Process Deployment Data
                driveDataType(self.deployDataFile)
            elif(self.rxData[3] == 3):
                # Process HQ Picture
                # PicRes 0 - LQ 1 - HQ
                drivePic(self.HQPicFile, 1, self.rxData[4])
            elif(self.rxData[3] == 4):
                # Process LQ Picture
                # PicRes 0 - LQ 1 - HQ
                drivePic(self.LQPicFile, 0, self.rxData[4])
            elif(self.rxData[3] == 5):
                # Add TX window to file
                addTXWindow()
            else:
                return
        else:
            #turn off tx
            if(self.rxData[1] == 0):
                canTX = False
            #take pic
            elif(self.rxData[2] == 1):
                #photo.Camera()
                pass
            #deploy boom
            elif(self.rxData[3] == 1):
                #boom.boomDeployer()
                pass
            elif(self.rxData[4] == 1):
                #reboot pi, send command to adruino
                pass
            else:
                return
    
    def driveDataType (self, dataFile):   
        '''
        Function if we are processing a datatype
        '''
        fdata = open(dataFile, 'r')
        line = f.readline()
                
        lastTXofDT = self.getFlagsTimestamp()
        
        counter = 0
        # '@' indicates EOF
        while line[0] != '@':
            if line[0] == '#':
                # Do Nothing, line commented
                pass
            elif line[0] == ' ':
                # DO Nothing, Line empty
                pass
            else:
                line = line.split(', ')
                if int(line[0]) < lastTXofDT:
                    # Line alredy transmitted
                    pass
                else:
                    counterInner = 0
                    while counterInner < len(line):
                        self.dataList[counter][counterInner] = line[counterInner]
                        counterInner = counterInner + 1
                    counter = counter + 1
            line = f.readline()
            line = line.replace('\n', '')
        
        numLines = self.packetize(False)
    
    def drivePic (self, dataFile, picRes, picNum):
        '''
        function if we are processing a  picture
        PicRes 0 - LQ 1 - HQ
        '''
        data = [()]
        
        ### TODO: getPicture no longer defined since deprecation of database
        data = self.getPicture(picNum, picRes)

        numLines = self.packetize(True)
 
    def getFlagsTimestamp(self):
        f_flags = open(self.flagsFile, 'r')
        allLines = f_flags.readlines()
        lastTX = allLines(self.rxData[3])
        return lastTX
           
    def packetize(self, isPic):
        """
        Write to file 
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

            for record in self.dataList:
                for value in record:
                
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
                #Don't need this anymore I updated my code so it doesn't use this any more -Shawn
            #f.write('@')
            #Don't add an extra line at the end of the file as we will TXService code will send it as data, and we dont wanna do that. -Shawn
            #f.write('\n')
        f.write(str(linesTotal))
        f.close()
        return linesTotal 

    def wipeTxFile():
        file = open(self.outputFile, "r+")
        file.truncate(0)
        file.close()        
    
'''
timestamp';' datapacket
timestamp';'     
'''
    
### TODO: Add Command functionality
### TODO: Add processing of picture (getPicture function, and picture functionality in packetize)
### TODO: Process AX25 Packets
### TODO: put all files in the same directory as the c code.
