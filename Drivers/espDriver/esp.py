#this is the foundation code for the esp driver. It NEEDS to be tested and we need to add in some more getters. The way the code is set
#up you should just be able to copy the getCurrent func change the name, the command, and the convertion factor. (See the i2c data sheet for 
#esp for the last two.) 
import smbus

class ESP:
    #this sets up i2c commincation. 
    def __init__(self):
        self.__DEVICE_BUS = 1
        self.__DEVICE_ADDR = 0x18
        self.__RegisterADR = 0x00
        self.__bus = smbus.SMBus(DEVICE_BUS)
    
    #we will write many getters simular to this one they will call the startRead func and then pass the right command to it so we can start 
    #the commication. It will then return the two bits it reads. 
    def getCurrent():
        super().__init__("ESP")
        return __startRead(1) * 0.0023394775#this is the convertion value. See the data sheet. 

    #this starts read commands to the ESP, will package the command for us. 
    def __startRead(command)
    #this code starts the command prosses, for read commands it is address bit shifted left by one, then the command, and then address bit 
    #shifted right by one.
    #Note: you may have to wait for an acknowledge bit, but this is stander i2c proticol so I'm not sure if python does it automaticly. 
        tempAddress = self.__DEVICE_ADDR << 1
        bus.write_byte_data(self.__DEVICE_ADDR, self.__RegisterADR, tempAddress)
        bus.write_byte_data(self.__DEVICE_ADDR, self.__RegisterADR, command)
        tempAddress = self.__DEVICE_ADDR >> 1
        bus.write_byte_data(self.__DEVICE_ADDR, self.__RegisterADR, tempAddress)
        #the read command always retruns two bytes. 
        return bus.read_i2c_block_data(self.__DEVICE_ADDR, self.__RegisterADR, 2)