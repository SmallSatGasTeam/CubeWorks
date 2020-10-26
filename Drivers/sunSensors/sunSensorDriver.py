from Drivers.Driver import Driver
from Drivers.adc import ADC_Driver
from time import sleep
class sunSensor(Driver):
    """
    This class calls the ADC driver and asks for data from the UV channel
    """
    adc = ADC_Driver.ADC()
    adcChannel = [5, 4, 0, 2, 3]
    voltageList = []

    def __init__(self):
        super().__init__("Sun Sensor")

    def read(self):
        """
        This function calls the read function of the ADC for each channel a sun sensor has and return a list of the voltages
        """
        self.voltageList = []
        for i in range(0, 5):
            self.voltageList.append(self.adc.read(self.adcChannel[i]))
            #print(self.adcChannel[i])
            #print(self.adc.read(5))
            #sleep(.1)
        return self.voltageList
