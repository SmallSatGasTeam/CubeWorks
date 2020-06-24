from Drivers.Driver import Driver
import smbus

class AntennaDoor(Driver):

    def __init__(self):
        super().__init__("AntennaDoor") #Calls parent constructor

        #Setup I2C bus for communication
        self.DEVICE_BUS = 1
        self.DEVICE_ADDR = 0x33
        self.RegisterADR = 0x00 # I do not know what this means or what it should be
        self.bus = smbus.SMBus(self.DEVICE_BUS)
      
    def readDoorStatus():
      #returns the status of all 4 antenna doors
      doorStatus = bus.read_i2c_block_data(self.DEVICE_ADDR, self.RegisterADR, 1)
      return doorStatus

