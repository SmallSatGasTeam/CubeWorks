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
spi_ch = 0
spi = spidev.SpiDev()
# spi.open(bus, device)
spi.open(0, spi_ch)


class ADC(Driver):
    # these are the pins for miso, mosi, cs, clk.
    # these are were the board is hooked up
    clkPin = 18
    misoPin = 23
    mosiPin = 24
    csPin = 25

    LOW = GPIO.LOW
    HIGH = GPIO.HIGH
    # there are 0-5 channels with this variable be sure to include 0
    numOfChannels = 5
    # this
    adcList = []

    def __init__(self):
        super().__init__("adc")

    def setupPins(self):
        # this method sets up all the pins to communicate with the ADC
        GPIO.setmode(GPIO.BOARD)
        # mosi = master out slave in
        GPIO.setup(self.mosiPin, GPIO.OUT)
        # miso = master in slave out
        GPIO.setup(self.misoPin, GPIO.IN)
        # clk = serial clock
        GPIO.setup(self.clkPin, GPIO.OUT)
        # disable spidev's chip select. we need to manage this manually
        spi.no_cs = True
        # cs = chip select
        GPIO.setup(self.csPin, GPIO.OUT, initial=GPIO.HIGH)

    def sendAndRecivBits(self, adcChannel):
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

    def read(self):
        # setup the GPIO pins for the adc
        self.setupPins()
        # send signal to the slave
        for i in range(0, 5):
            self.adcList.append(self.sendAndRecivBits(i))
        GPIO.cleanup()
        return self.adcList
