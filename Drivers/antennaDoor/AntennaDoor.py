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
        self.RegisterADR = 0x00 # I do not know what this means or what it should be
        self.bus = smbus.SMBus(self.DEVICE_BUS)
      
    def readDoorStatus(self):
        """
        returns the status of all 4 antenna doors
        doorStatus = self.bus.read_i2c_block_data(self.DEVICE_ADDR, self.RegisterADR, 1)
        NOTE: THE BELOW LINE IS ONLY USED WHEN THE ANTENNA IS NOT CONNECTED
        REMOVE THE BELOW LINE FOR FLIGHT UNIT, UNCOMMENT THE ABOVE doorStatus LINE AND DEBUG
        """
        doorStatus = (1,1,1,1)
        return doorStatus

