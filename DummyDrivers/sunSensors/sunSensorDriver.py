from DummyDrivers.Driver import Driver
from DummyDrivers.adc import ADC_Driver

class sunSensor(Driver):
    """
    This class calls the ADC driver and asks for data from the UV channel
    """
    #adc = ADC_Driver.ADC()
    #adcChannel = [5, 4, 2, 3, 0]
    #voltageList = []

    def __init__(self):
        super().__init__("Sun Sensor")
        self.voltageList=[]

    def read(self):
        """
        This function calls the read function of the ADC for each channel a sun sensor has and return a list of the voltages
        """
        for i in range(0, 5):
            self.voltageList.append(51)

        return self.voltageList
