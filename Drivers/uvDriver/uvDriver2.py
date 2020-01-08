from Drivers.Driver import Driver

    
class uvSensor(Driver):
    def __init__(self):
        super().__init__("uvSensor")

    #adcData is a 12 bit binary string
    def read(self):
        # adc lsb found by Vrefin / 4096 which is 5V / 4096
        voltageStep = 0.001220703125

        # converts the 12 bit binary number to decimal
        #TODO Find how to get the adc data
        numberOfSteps = int('''adcfunctioncall''', 2)

        # calculate the output voltage from UV sensor
        voltage = numberOfSteps * voltageStep

        # calculate the uvPower
        uvPower = voltage * 1000 / 485.9
        return uvPower

