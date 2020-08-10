from DummyDrivers.Driver import Driver
import spidev
import RPi.GPIO as GPIO


class ADC(Driver):
    """
    This class interfaces with the ADC to read the voltage on a specified channel
    """
    csPin = 22
      
    spi_ch = 0
    spi = spidev.SpiDev()
    # spi.open(bus, device)
    spi.open(0, spi_ch)
    # disable spidev's chip select. we need to manage this manually
    spi.no_cs = True
    # cs = chip select
         
    def __init__ (self):
        # these are the pins for miso, mosi, cs, clk.
        # these are were the board is hooked up
        super().__init__("ADC")
        
    
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.csPin, GPIO.OUT, initial=GPIO.HIGH)

    def read(self, channel):
        """
        Sends a read command with a specified channel and then returns the reply from the ADC
        """
        # Start the read with both clock and chip select low
        GPIO.output(self.csPin, GPIO.LOW)

        # the following creates a message to send to the slave
        msg = (channel << 3)
        msg = [msg, 0b00000000]
        # the followin
        reply = self.spi.xfer2(msg)

        # set the clock and chip select to high to end message
        GPIO.output(self.csPin, GPIO.HIGH)
         
        # convert the reply from 12 bits stored in two bytes to a voltage
        # 12 bit data:  byte 0 [0 0 0 0 MSB d11 d10 d9] byte 1 [d8 d7 d6 d5 d4 d3 d2 LSB]
        # Each LSB represents 3.3/4096 volts
        return(reply[1] + (reply[0] * 256))*(3.3/4096)
