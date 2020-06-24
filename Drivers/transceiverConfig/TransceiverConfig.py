from Drivers.Driver import Driver

class TransceiverConfig(Driver):
  def __init__(self):
    """
    The purpose of this driver is to modify the configuration of the Endurosat UHF Transceiver. 
    It does not have anything to do with sending packets over the radio.
    The only configuration option that our flight logic requires is the ability to turn on and off morse code beacons.
    """
    
