from Drivers.Driver import Driver
import smbus
from time import sleep

class AntennaDoor(Driver):

    def __init__(self):
        super().__init__("AntennaDoor") #Calls parent constructor
        """
        Sets up I2C bus for communication
        """
        self.DEVICE_BUS = 1
        self.DEVICE_ADDR = 0x33
        self.bus = smbus.SMBus(self.DEVICE_BUS)
        self.doorStatus = -1
        sleep(1)

    def readDoorStatus(self):
        """
        Reads the I2C response from the antenna.
        The first 4 bits of the first byte represent the 4 antenna doors. 0 is not deployed, 1 is deployed. 
        Uses bitwise "or" to check if all 4 antenna doors are deployed. If yes, set deployed True. If any
        doors are undeployed, set deployed False.
        """
        # This command returns one byte from the antenna. Check the antenna manual for an explanation of the bytes.
        self.doorStatus = self.bus.read_byte(self.DEVICE_ADDR)
        doorBits = self.doorStatus
        print("Decimal value from antenna: ", doorBits)
        deployed = False
        # decimal representation of 00001111
        bitmask = 15
        bitwise = (doorBits | bitmask)
        print("Bitwise result: ", bitwise)
        if(bitwise == 255):
            deployed = True
        else :
            deployed = False
        print("deployed", deployed)
        return deployed
    
    #this is the command to deploy the anntenna
    def deployAntennaMain(self):
        try :
            self.doorStatus = self.bus.read_byte(self.DEVICE_ADDR)
        except :
            self.doorStatus = -1
            
        print("\t____Deploying the Antenna____")
        if(self.doorStatus == 0):
            try :
                self.bus.write_byte(self.DEVICE_ADDR,0x1F)
            except :
                print("Failed to run 1")
        else :
            try :
                self.bus.write_byte(self.DEVICE_ADDR,0x2F)
            except :
                print("Failed to run 2")
        print("\t____Deployed the Antenna____")
