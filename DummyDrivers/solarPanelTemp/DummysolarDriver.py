from DummyDrivers.Driver import Driver
import spidev
import RPi.GPIO as GPIO


class TempSensor(Driver):
    """
    This class interfaces with the ADC to read a specified channel
    """
    def __init__ (self):
        super().__init__("ADC")

    def read(self):
        """
        Sends a read command with a specified channel and then returns the reply from the ADC
        """
        return [23,24]
