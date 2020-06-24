from Drivers.Driver import Driver
from Drivers.adc import ADC_Driver

class UVDriver(Driver):
  """
  This class calls the ADC driver and asks for data from the UV channel
  """
  adc = ADC_Driver.ADC()
  uv_channel = 1  #The channel on the ADC that th UV sensor is connected to
  
  def __init__(self):
    super().__init__("UVDriver")
  
  def read(self):
    """
    This function calls the read function of the ADC with the channel for the uv sensor
    """
    return self.adc.read(self.uv_channel)


class sunSensor(Driver):
    """
    This class calls the ADC driver and asks for data from the UV channel
    """
    adc = ADC_Driver.ADC()
    adcChannel = [5, 4, 2, 3, 0]
    voltageList = []

    def __init__(self):
        super().__init__("Sun Sensor")

    def read(self):
        """
        This function calls the read function of the ADC for each channel a sun sensor has and return a list of the voltages
        """
        for i in range(0, 4):
            self.voltageList.append(adc.read(adcChannel[i]))

        return self.voltageList
