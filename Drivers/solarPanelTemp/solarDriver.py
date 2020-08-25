from Drivers.Driver import Driver
import spidev
import RPi.GPIO as GPIO
from time import sleep

class TempSensor(Driver):
    """
    This class returns the temperature sensor values for both Endurosat solar panels.
    """

    GPIO.setmode(GPIO.BCM)

    spi0 = spidev.SpiDev()
    # open SPI to Temp sensor0
    spi0.open(0, 1)
    spi0.max_speed_hz = 10
    spi0.no_cs = True
    # BOARD 26 is GPIO 7
    spi0_cs = 7
    GPIO.setup(spi0_cs, GPIO.OUT, initial=GPIO.HIGH)

    spi1 = spidev.SpiDev()
    # open SPI to Temp sensor1
    spi1.open(0, 1)
    spi1.max_speed_hz = 10
    spi1.no_cs = True
    # BOARD 24 is GPIO 8
    spi1_cs = 8
    GPIO.setup(spi1_cs, GPIO.OUT, initial=GPIO.HIGH)

    def __init__ (self):
        #super().__init__("ADC")
        pass

    def read(self):
        """
        Sends a read command with a specified channel and then returns the reply from the ADC
        """
        GPIO.output(self.spi0_cs, GPIO.LOW)
        temp0_raw = self.spi0.readbytes(2)  #We need just the first 13 bits, as the last three bits of the 16 bit(2 byte) word are not used
        GPIO.output(self.spi0_cs, GPIO.HIGH)
        #This function converts the two bytes to the temperature value. The data is stored as two bytes where T13 is the most significant bit
        #| T13 T12 T11 T10 T9 T8 T7 T6 |  | T5 T4 T3 T2 T1 1 1 1 |
        temp0 = ((temp0_raw[0] * 32) + (temp0_raw[1] >> 3))* 0.0625

        GPIO.output(self.spi1_cs, GPIO.LOW)
        temp1_raw = self.spi1.readbytes(2)  #We need just the first 13 bits, as the last three bits of the 16 bit(2 byte) word are not used
        GPIO.output(self.spi1_cs, GPIO.HIGH)
        #This function converts the two bytes to the temperature value. The data is stored as two bytes where T13 is the most significant bit
        #| T13 T12 T11 T10 T9 T8 T7 T6 |  | T5 T4 T3 T2 T1 1 1 1 |
        temp1 = ((temp1_raw[0] *32) + (temp1_raw[1] >> 3))* 0.0625
 
        return [temp0, temp1]
