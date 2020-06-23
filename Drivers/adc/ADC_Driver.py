from Drivers.Driver import Driver
import spidev
import RPi.GPIO as GPIO

"""
    ***IMPORTANT***
    NOTE: Ben, I believe that spi_ch is the correct value of the channel
    if it is not just send me a message with the value and i can fix 
    that. Same with the bus in spi.open(). i just made the best judgment 
    call i could.
"""


class ADC(Driver):
    """
    This class interfaces with the ADC to read a specified channel
    """
    clkPin = 23
    misoPin = 21
    mosiPin = 19
    csPin = 22
      
    LOW = GPIO.LOW
    HIGH = GPIO.HIGH
    # there are 0-5 channels with this variable be sure to include 0
    numOfChannels = 5
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

    def sendAndRecivBits(self, adcChannel):
        """
        Sends a read command with a specified channel and then returns the reply from the ADC
        """
        # Start the read with both clock and chip select low
        GPIO.output(self.csPin, self.LOW)
        GPIO.output(self.clkPin, self.LOW)

        # the following creates a message to send to the slave
        msg = 0b11
        msg = ((msg << 1) + adcChannel) << 5
        msg = [msg, 0b00000000]
        # the followin
        reply = spi.xfer2(msg)

        # set the clock and chip select to high to end message
        GPIO.output(self.csPin, self.HIGH)
        GPIO.output(self.clkPin, self.HIGH)
        return reply

    def calculate(self, unconvertedNum):
        """
        Converts the 12 bit reply from the ADC to the voltage value between 0 and 3.3
        """
        voltageStep = 0.000805664062

        # converts the 12 bit binary number to decimal
        numberOfSteps = float(unconvertedNum * 10000)

        # calculate the output voltage from UV sensor
        voltage = numberOfSteps * voltageStep
        return voltage

    def read(self, channel):
        """
        Calls functions to set up the pins for communication, read the 12 bit value from the ADC, and converts the value to a voltage float. Returns the float.
        """
        spi_ch = 0
        spi = spidev.SpiDev()
        # spi.open(bus, device)
        spi.open(0, spi_ch)
        # disable spidev's chip select. we need to manage this manually
        spi.no_cs = True
        # cs = chip select
         
        # send signal to and receive from the slave
        adcChannelOutput = self.calculate(self.sendAndRecivBits(channel))
        #GPIO.cleanup()
        return adcChannelOutput
