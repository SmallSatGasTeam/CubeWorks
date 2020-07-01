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
