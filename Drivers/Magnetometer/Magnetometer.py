#Make sure the following libraries are installed:
#   sudo pip3 install RPI.GPIO
#   sudo pip3 install adafruit-blinka
#   sudo pip3 install adafruit-circuitpython-lsm303-accel
#   For LSM303AGR:
#     sudo pip3 install adafruit-circuitpython-lis2mdl
#   For LSM303DLH:
#     sudo pip3 install adafruit-circuitpython-lsm303dlh-mag

from Drivers.Driver import Driver
import board
import busio
#for LSM303AGR
import adafruit_lis2mdl
#for LSM303DLH
#import adafruit_lsm303dlh_mag

class Magnetometer(Driver):
  #Set up I2C link
  i2c = busio.I2C(board.SCL, board.SDA)
    
  def __init__(self):
    super().__init__("Magnetometer")
    
  def read(self) :
    #Set up link to magnetometer
    #for LSM303AGR
    #mag = adafruit_lis2mdl.LIS2MDL(self.i2c)
    #for LSM303DLH
    mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(self.i2c)
    return mag.magnetic
