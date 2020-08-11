#EPS Driver, not tested against hardware yet
from DummyDrivers.Driver import Driver
#circurt bus??? maybe use that

class EPS(Driver):
    #this sets up i2c commincation.
    def __init__(self):
        super().__init__("EPS") #Calls parent constructor


    def enableRaw(self):
        #This method enables RAW battery output from the EPS
        #The command is 3 bytes device address left-shifted by one bit, the command, and the state
        tempAddress = self.DEVICE_ADDR << 1
        self.bus.write_byte_data(self.DEVICE_ADDR, self.RegisterADR, tempAddress)
        self.bus.write_byte_data(self.DEVICE_ADDR, self.RegisterADR, 0x01) #Battery Raw BUS
        self.bus.write_byte_data(self.DEVICE_ADDR, self.RegisterADR, 0x03) #Forced ON state

    def disableRaw(self):
        #This method disables RAW battery output from the EPS
        #The command is 3 bytes device address left-shifted by one bit, the command, and the state
        tempAddress = self.DEVICE_ADDR << 1
        self.bus.write_byte_data(self.DEVICE_ADDR, self.RegisterADR, tempAddress)
        self.bus.write_byte_data(self.DEVICE_ADDR, self.RegisterADR, 0x01) #Battery Raw BUS
        self.bus.write_byte_data(self.DEVICE_ADDR, self.RegisterADR, 0x02) #Forced OFF state <-- Do we want to use Forced OFF/ON or Auto OFF/ON?

    def read(self):
        #returns nothing since there are so many different things we could read, use other methods instead
        pass

    def __startRead(command):
        #This method sends read commands to the EPS. Shawn wrote it, I assume it's correct --Logan
        #this code starts the command process, for read commands it is address bit shifted left by one, then the command, and then address bit
        #shifted right by one.
        #Note: you may have to wait for an acknowledge bit, but this is stander i2c proticol so I'm not sure if python does it automatically.
        tempAddress = self.DEVICE_ADDR << 1
        self.bus.write_byte_data(self.DEVICE_ADDR, self.RegisterADR, tempAddress)
        self.bus.write_byte_data(self.DEVICE_ADDR, self.RegisterADR, command) # do you need do convert the int to hex somehow?
        tempAddress = self.DEVICE_ADDR >> 1
        self.bus.write_byte_data(self.DEVICE_ADDR, self.RegisterADR, tempAddress)
        #the read command always returns two bytes.
        return self.bus.read_i2c_block_data(self.DEVICE_ADDR, self.RegisterADR, 2)

    #Getter calls read method, returns converted data - all values are converted 12 bits, even though 2 bytes returned
    def getMCUTemp(self):
        #super().__init__("ESP") <-- Shawn had this in here, I don't understand why it's here so I'm commenting it out and leaving it out of other ones
        temp = 15
        temp = ((temp *0.0006103516) - 0.986)/0.00355
        return temp #done with multiple lines because of complicated conversion

    def getCell1Temp(self):
        return 11*0.00390625 #Reads data of specified type, sets up conversion factor to 'C

    def getCell2Temp(self):
        return 12*0.00390625 #Reads data of specified type, sets up conversion factor to 'C

    def getBusVoltage(self):
        #return 13 * 0.0023394775 #Reads data of specified type, sets up conversion factor to V
        return 3.5

    def getBusCurrent(self):
        return 14 * 0.0030517578 #Reads data of specified type, sets up conversion factor to A

    def getBCRVoltage(self):
        return 15 * 0.0023394775 #Reads data of specified type, sets up conversion factor to V

    def getBCRCurrent(self):
        return 16 * 0.0015258789 #Reads data of specified type, sets up conversion factor to A

    def get3V3Current(self):
        return 17 * 0.0020345052 #Reads data of specified type, sets up conversion factor to A

    def get5VCurrent(self):
        return 18 * 0.0020345052 #Reads data of specified type, sets up conversion factor to A

    def getSPXVoltage(self):
        return 19 * 0.0024414063 #Reads data of specified type, sets up conversion factor to V

    def getSPXMinusCurrent(self):
        return 20 * 0.0006103516 #Reads data of specified type, sets up conversion factor to A

    def getSPXPlusCurrent(self):
        return 21 * 0.0006103516 #Reads data of specified type, sets up conversion factor to A

    def getSPYVoltage(self):
        return 22 * 0.0024414063 #Reads data of specified type, sets up conversion factor to V

    def getSPYMinusCurrent(self):
        return 23 * 0.0006103516 #Reads data of specified type, sets up conversion factor to A

    def getSPYPlusCurrent(self):
        return 24 * 0.0006103516 #Reads data of specified type, sets up conversion factor to A

    def getSPZVoltage(self):
        return 25 * 0.0024414063 #Reads data of specified type, sets up conversion factor to V

    def getSPZPlusVoltage(self):
        return 26 * 0.0006103516
