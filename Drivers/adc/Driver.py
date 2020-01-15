from Drivers.Driver import Driver
from typing import List, Tuple
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
    
class adc(Driver):
    def __init__(self):
        """Constructor for the ADC driver

        Todo:
            * Change the number of numChannels
        """
        super().__init__("adc")
        self.SPI_PORT: int   = 0
        self.SPI_DEVICE: int = 0
        self.numChannels: int   = 8
        self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE))

    def read(self, channel: int = -1) -> List[int]:
        """Read from the ADC

        Returns: 
            list of int: the readings from each of the numChannels of the ADC
        """

        if channel > -1:
            return self.mcp.read_adc(channel)
        else:
            return [self.mcp.read_adc(i) for i in range(self.numChannels)]

