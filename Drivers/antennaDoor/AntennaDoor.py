from Drivers.Driver import Driver
import smbus

class AntennaDoor(Driver):

    def __init__(self):
        super().__init__("AntennaDoor") #Calls parent constructor
        """
        Sets up I2C bus for communication
        """
        self.DEVICE_BUS = 1
        self.DEVICE_ADDR = 0x33
        self.RegisterADR = 0x00
        self.bus = smbus.SMBus(self.DEVICE_BUS)
      
    def readDoorStatus(self):
        """
        Reads the I2C response from the antenna. Takes the first byte of the response. 
        The first 4 bits of the first byte represent the 4 antenna doors. 0 is not deployed, 1 is deployed. 
        Uses bitwise "or" to check if all 4 antenna doors are deployed. If yes, set deployed True. If any
        doors are undeployed, set deployed False.
        """
        # This command passes in the device address, register address, and "4" because we expect a 4 byte response
        doorStatus = self.bus.read_i2c_block_data(self.DEVICE_ADDR, self.RegisterADR, 4)
        print(doorStatus)
        doorBits = doorStatus[0]
        print("doorBits", doorBits)
        deployed = False
        print("bitwise", doorBits | 00001111)
        if(doorBits | 00001111 == 11111111):
            deployed = True
        else
            deployed = False
        #doorStatus = (1,1,1,1)
        print("deployed", deployed)
        return deployed
