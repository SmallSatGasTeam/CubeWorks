### This test activates the primary antenna deployment system over I2C using Algorithm 2 ###
import smbus
from time import sleep

DEVICE_BUS = 1
DEVICE_ADDR = 0x33
bus = smbus.SMBus(self.DEVICE_BUS)
sleep(1)
print("\t____Deploying the Antenna____")
bus.write_byte(self.DEVICE_ADDR,0x2F)
print("\t____Deployed the Antenna____")
