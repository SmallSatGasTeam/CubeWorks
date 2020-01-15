from Drivers.Driver import Driver
from Drivers.adc.Driver import adc as ADC
    
class uvSensor(Driver):
    def __init__(self):
        super().__init__("uvSensor")

    #adcData is a 12 bit binary string
    def read(self):
        # calculate the output voltage from UV sensor
        voltage = ADC.read(3)

        # calculate the uvPower
        uvPower = voltage * 1000 / 485.9
        return uvPower

