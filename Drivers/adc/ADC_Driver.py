from Drivers.Driver import Driver
import spidev
import RPi.GPIO as GPIO


class ADC(Driver):
    """
    This class interfaces with the ADC to read a specified channel
    """
    clkPin = 23
    misoPin = 21
    mosiPin = 19
    csPin = 22
      
    # there are 0-5 channels with this variable be sure to include 0
    numOfChannels = 5
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
        # mosi = master out slave in
        GPIO.setup(self.mosiPin, GPIO.OUT)
        # miso = master in slave out
        GPIO.setup(self.misoPin, GPIO.IN)
        # clk = serial clock
        GPIO.setup(self.clkPin, GPIO.OUT)
        GPIO.setup(self.csPin, GPIO.OUT, initial=GPIO.HIGH)

    def read(self, channel):
        """
        Sends a read command with a specified channel and then returns the reply from the ADC
        """
        # Start the read with both clock and chip select low
        GPIO.output(self.csPin, GPIO.LOW)
        GPIO.output(self.clkPin, GPIO.LOW)

        # the following creates a message to send to the slave
        msg = 0b11
        msg = ((msg << 1) + adcChannel) << 5
        msg = [msg, 0b00000000]
        # the followin
        reply = self.spi.xfer2(msg)

        # set the clock and chip select to high to end message
        GPIO.output(self.csPin, GPIO.HIGH)
        GPIO.output(self.clkPin, GPIO.HIGH)
         
        # convert the reply from 12 bits stored in two bytes to a voltage
        # 12 bit data:  byte 1 [0 0 0 0 MSB d11 d10 d9] byte 0 [d8 d7 d6 d5 d4 d3 d2 LSB]
        # Each LSB represents 3.3/4096 volts
        return(reply[0] + (reply[1] * 512))*(3.3/4096)
