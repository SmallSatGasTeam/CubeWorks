from DummyDrivers.Driver import Driver
#from Drivers.adc import ADC_Driver

class sunSensor(Driver):
    """
    This class calls the ADC driver and asks for data from the UV channel
    """

    def __init__(self):
        super().__init__("Sun Sensor")

    def read(self):
        """
        This function calls the read function of the ADC for each channel a sun sensor has and return a list of the voltages
        """
        voltageList = []
        for i in range(0, 5):
            voltageList.append(1.3)

        return voltageList
