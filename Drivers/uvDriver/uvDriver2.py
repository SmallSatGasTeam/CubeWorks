from Drivers.Driver import Driver


class uvSensor(Driver):
    def __init__(self):
        super().__init__("uvSensor")

    def read(self,adcData):
        # adc lsb found by Vrefin / 4096, 5V / 4096
        voltageStep = 0.001220703125
        # converts the 12 bit binary number to decimal
        numberOfSteps = int(adcData, 2)
        # calculate the output voltage from UV sensor
        voltage = round(numberOfSteps * voltageStep, 3)
        # turn voltage into photocurrent
        photoCurrent = round(voltage / 4.3 * 1000, 4)
        # turn photocurrent into uv index
        uvPower = round(photoCurrent/113,3)
        return uvPower
