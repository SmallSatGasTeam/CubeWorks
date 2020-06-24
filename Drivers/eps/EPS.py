#EPS Driver, not tested against hardware yet
from Drivers.Driver import Driver
import smbus
#circurt bus??? maybe use that

class EPS(Driver):
    #this sets up i2c commincation.
    def __init__(self):
        super().__init__("EPS") #Calls parent constructor

        #Setup I2C bus for communication
        self.DEVICE_BUS = 1
        self.DEVICE_ADDR = 0x18
        self.RegisterADR = 0x00
        self.bus = smbus.SMBus(DEVICE_BUS)

    def enableRaw(self):
        #This method enables RAW battery output from the EPS
        #The command is 3 bytes device address left-shifted by one bit, the command, and the state
        tempAddress = self.__DEVICE_ADDR << 1
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
        return

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
        return self.bus.read_i2c_block_data(self.__DEVICE_ADDR, self.__RegisterADR, 2)

    #Getter calls read method, returns converted data - all values are converted 12 bits, even though 2 bytes returned
    def getMCUTemp():
        #super().__init__("ESP") <-- Shawn had this in here, I don't understand why it's here so I'm commenting it out and leaving it out of other ones
        temp = startRead(18)
        temp = ((temp *0.0006103516)– 0.986)/0.00355
        return temp #done with multiple lines because of complicated conversion
    def getCell1Temp():
        return __startRead(19)*0.00390625 #Reads data of specified type, sets up conversion factor to 'C

    def getCell2Temp():
        return __startRead(20)*0.00390625 #Reads data of specified type, sets up conversion factor to 'C

    def getBusVoltage():
        return __startRead(1) * 0.0023394775 #Reads data of specified type, sets up conversion factor to V

    def getBusCurrent():
        return __startRead(2) * 0.0030517578 #Reads data of specified type, sets up conversion factor to A

    def getBCRVoltage():
        return __startRead(3) * 0.0023394775 #Reads data of specified type, sets up conversion factor to V

    def getBCRCurrent():
        return __startRead(4) * 0.0015258789 #Reads data of specified type, sets up conversion factor to A

    def get3V3Current():
        return __startRead(14) * 0.0020345052 #Reads data of specified type, sets up conversion factor to A

    def get5VCurrent():
        return __startRead(15) * 0.0020345052 #Reads data of specified type, sets up conversion factor to A

    def getSPXVoltage():
        return __startRead(5) * 0.0024414063 #Reads data of specified type, sets up conversion factor to V

    def getSPXMinusCurrent():
        return __startRead(6) * 0.0006103516 #Reads data of specified type, sets up conversion factor to A

    def getSPXPlusCurrent():
        return __startRead(7) * 0.0006103516 #Reads data of specified type, sets up conversion factor to A

    def getSPYVoltage():
        return __startRead(8) * 0.0024414063 #Reads data of specified type, sets up conversion factor to V

    def getSPYMinusCurrent():
        return __startRead(9) * 0.0006103516 #Reads data of specified type, sets up conversion factor to A

    def getSPYPlusCurrent():
        return __startRead(10) * 0.0006103516 #Reads data of specified type, sets up conversion factor to A

    def getSPZVoltage():
        return __startRead(11) * 0.0024414063 #Reads data of specified type, sets up conversion factor to V

