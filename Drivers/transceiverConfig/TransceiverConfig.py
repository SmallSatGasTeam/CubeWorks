from Drivers.Driver import Driver
import serial

class TransceiverConfig(Driver):
  def __init__(self):
    """
    The purpose of this driver is to modify the configuration of the Endurosat UHF Transceiver. 
    It does not have anything to do with sending packets over the radio.
    We need the ability to turn on and off the beacon, turn on low power mode, and read the internal temp sensor.
    See Page 25 of the Endurosat UHF Transceiver Type II Manual Rev 1.8 document for the SCW bit description.
    
    ***Note: ALL ES+ commands need to be changed to reflect the address of the transceiver - currently set to 23***
    ***Potentially need to add CRC32 checksum functionality***
    """
    super().__init__("TransceiverConfig")
    
  def writeData(self, input):
    """
    Writes the input to the transceiver over UART
    """
    ser = serial.Serial('/dev/serial0', 115200)
    data = input                              #Set data to the character 'a', 0x61 or 01100001
    ser.write(data) #Send the data
    #response = ser.read(128)
    ser.close()
    #return response
  
  def setBeaconOn(self):
    """
    Turns on the morse beacon. Leaves all values at default except beacon.
    Binary SCW: 11001101000001
    Hex SCW: 3341
    """
    self.writeData(b'ES+W23003341\r')
  
  def setBeaconOff(self):
    """
    Turns off the morse beacon. All values are back to default.
    Binary SCW: 11001100000001
    Hex SCW: 3301
    """
    self.writeData(b'ES+W23003301\r')

  def setLowPowerMode(self):
    """
    Turns on Low Power Mode. Note: Any ESTTC command can be used to bring the transceiver out of low power mode
    """
    self.writeData(b'ES+W23F4\r')

  def read(self):
    """
    Returns the temperature from the transceiver internal temp sensor
    """
    temp = self.writeData(b'ES+R230A\r')
    return temp
