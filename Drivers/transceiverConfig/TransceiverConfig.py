from Drivers.Driver import Driver

class TransceiverConfig(Driver):
  def __init__(self):
    """
    The purpose of this driver is to modify the configuration of the Endurosat UHF Transceiver. 
    It does not have anything to do with sending packets over the radio.
    The only configuration option that our flight logic requires is the ability to turn on and off morse code beacons.
    """
    super().__init__("TransceiverConfig")
    
  def setBeaconOn(self):
    """
    Turns on the morse beacon
    """
    
  
  def setBeaconOff(self):
    """
    Turns off the morse beacon
    """
    
  def read(self):
    """
    We don't need any data from the transceiver so this returns nothing
    """
    pass
