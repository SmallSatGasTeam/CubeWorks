from DummyDrivers.Driver import Driver

class UVDriver(Driver):
  """
  This class calls the ADC driver and asks for data from the UV channel
  """
  def __init__(self):
    super().__init__("UVDriver")

  def read(self):
    """
    This function calls the read function of the ADC with the channel for the uv sensor
    """
    return 0.5
