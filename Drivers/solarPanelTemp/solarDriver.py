from Drivers.Driver import Driver
import spidev
import RPi.GPIO as GPIO


class TempSensor(Driver):
    """
    This class interfaces with the ADC to read a specified channel
    """
      
    spi0 = spidev.SpiDev()
    # open SPI to Temp sensor0
    spi0.open(0, 0)
    
    spi1 = spidev.SpiDev()
    # open SPI to Temp sensor1
    spi1.open(0, 1)
         
    def __init__ (self):
        super().__init__("ADC")

    def read(self):
        """
        Sends a read command with a specified channel and then returns the reply from the ADC
        """
        temp0_raw = self.spi0.readbytes(2)  #We need just the first 13 bits, as the last three bits of the 16 bit(2 byte) word are not used

        #This function converts the two bytes to the temperature value. The data is stored as two bytes where T13 is the most significant bit
        #| T13 T12 T11 T10 T9 T8 T7 T6 |  | T5 T4 T3 T2 T1 1 1 1 |
        temp0 = ((temp0_raw[0] * 64) + (temp0_raw[1] >> 3))* 0.0625
        
        temp1_raw = self.spi1.readbytes(2)  #We need just the first 13 bits, as the last three bits of the 16 bit(2 byte) word are not used

        #This function converts the two bytes to the temperature value. The data is stored as two bytes where T13 is the most significant bit
        #| T13 T12 T11 T10 T9 T8 T7 T6 |  | T5 T4 T3 T2 T1 1 1 1 |
        temp1 = ((temp1_raw[0] * 64) + (temp1_raw[1] >> 3))* 0.0625
        
        return [temp0, temp1]
