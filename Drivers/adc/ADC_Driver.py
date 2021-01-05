from Drivers.Driver import Driver
import spidev
import RPi.GPIO as GPIO
from time import sleep

class ADC(Driver):
    """
    This class interfaces with the ADC to read the voltage on a specified channel
    """
    # Chip Select Pin. This is BOARD Pin 22, which is GPIO 25
    csPin = 25
     
    spi_ch = 0
    
    spi = spidev.SpiDev()
    # spi.open(bus, device)
    spi.open(0, spi_ch)
    # disable spidev's chip select. we need to manage this manually
    spi.no_cs = True
    spi.max_speed_hz = 1000
    # cs = chip select

    # Sleep after chip select delay
    csDelay = 0.01

    def __init__ (self):
        # these are the pins for miso, mosi, cs, clk.
        # these are where the board is hooked up
        super().__init__("ADC")
        
    
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.csPin, GPIO.OUT, initial=GPIO.HIGH)
        
        print("Initializing ADC")

    def read(self, channel):
        """
        Sends a read command with a specified channel and then returns the reply from the ADC
        """
        # Start the read with both clock and chip select low
        GPIO.output(self.csPin, GPIO.LOW)
        sleep(self.csDelay)
        msg = (channel << 3) 
        msg = [msg, 0b00000000]

        print("Channel: ", channel)
        print("Sent message: ", bin(msg[0]), bin(msg[1]))
        print("Spi channel: ", self.spi)

        reply = self.spi.xfer2(msg)
        value = (reply[1] + (reply[0] * 256))*(3.3/4096)
        # set the clock and chip select to high to end message
        GPIO.output(self.csPin, GPIO.HIGH)
        sleep(self.csDelay)
        return value

        # convert the reply from 12 bits stored in two bytes to a voltage
        # 12 bit data:  byte 0 [0 0 0 0 MSB d11 d10 d9] byte 1 [d8 d7 d6 d5 d4 d3 d2 LSB]
        # Each LSB represents 3.3/4096 volts

    def close(self):
        self.spi.close()
