from Drivers.Driver import Driver
import serial

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
    ser = serial.Serial ("/dev/ttyAMA0")               #Open named port 
    ser.baudrate = 115200                              #Set baud rate to 9600
    data = "ES+W23003321"                              #Set data to the character 'a', 0x61 or 01100001
    ser.write(data)                                    #Send the data
    ser.close()
  
  def setBeaconOff(self):
    """
    Turns off the morse beacon
    """
    
  def setLowPowerMode(self):
    """
    Turns on Low Power Mode. Note: Any ESTTC command can be used to bring the transceiver out of low power mode
    """
    
    
  def read(self):
    """
    We don't need any data from the transceiver so this returns nothing
    """
    pass
