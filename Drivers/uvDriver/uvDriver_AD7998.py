from Drivers.Driver import Driver
from Drivers.adc.ADC_Driver import adc
import RPi.GPIO as GPIO

class uvSensor(Driver):
    clkPin = 18
    misoPin = 23
    mosiPin = 24
    csPin = 25
    numBits = 12
    channel = 1
    LOW = GPIO.LOW
    HIGH = GPIO.HIGH

    def __init__(self):
        super().__init__("uvSensor")

    def setupSpiPins(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.mosiPin, GPIO.OUT)
        GPIO.setup(self.misoPin, GPIO.IN)
        GPIO.setup(self.clkPin, GPIO.OUT)
        GPIO.setup(self.csPin, GPIO.OUT, initial=GPIO.HIGH)

    def readAdc(self):
        LOW = GPIO.LOW
        HIGH = GPIO.HIGH
        # Datasheet says chip select must be pulled high between conversions
        GPIO.output(self.csPin, HIGH)
        # Start the read with both clock and chip select low
        GPIO.output(self.csPin, LOW)
        GPIO.output(self.clkPin, LOW)

        # read command is:
        # start bit = 1
        # single-ended comparison = 1 (vs. pseudo-differential)
        # channel num bit 2
        # channel num bit 1
        # channel num bit 0 (LSB)
        read_command = 0x12
        read_command |= self.channel

        self.sendBits(read_command, HIGH, LOW)

        adcValue = self.recvBits(HIGH, LOW)

        # Set chip select high to end the read
        GPIO.output(self.csPin, HIGH)

        return adcValue

    def sendBits(self, data, HIGH, LOW):
        ''' Sends 1 Byte or less of data'''

        data <<= (8 - self.numBits)

        for bit in range(self.numBits):
            pass
            # Set RPi's output pin high or low depending on highest bit of data field
            GPIO.output(self.mosiPin, )
        # Advance data to the next bit

        # Clock pulse
        GPIO.output(self.clkPin, HIGH)
        GPIO.output(self.clkPin, LOW)

    def recvBits(self, HIGH, LOW):
        retVal = adc.read(pyb.ADC(self.misoPin))

        return retVal

    # adcData is a 12 bit binary string
    def read(self):
        self.setUp()
        # sets up a pin for MISO
        adcInput = pyb.adc(pyb.ADC(self.misoPin))
        # adc lsb found by Vrefin / 4096 which is 5V / 4096
        voltageStep = 0.000805664062

        # converts the 12 bit binary number to decimal
        voltage = adc.read(adcInput)
        numberOfSteps = float(voltage * 10000)

        # calculate the output voltage from UV sensor
        voltage = numberOfSteps * voltageStep

        if voltage > 3.2:
            uvPower = True
        else:
            uvPower = False
        return uvPower


