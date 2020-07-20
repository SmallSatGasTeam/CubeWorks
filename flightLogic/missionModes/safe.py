import smbus
import Drivers.eps.EPS as EPS
import asyncio
#####################################################################################
#All this class does is tell the arduino to shut off the pi for the specified amount
#of time.
#times: to pass to the run func
#pass 1 for 1 min
#pass 2 for 2 min
#pass 3 for 3 min
#pass 10 for an hour
#pass 60 for 6 hours
#pass 120 for 12 hours
#pass 24 for a day
#####################################################################################
class safe:
    def __init__(self):
        #Setup I2C bus for communication
        self.DEVICE_BUS = 1
        self.__beetle = 0x08
        self.RegisterADR = 0x00
        self.bus = smbus.SMBus(self.DEVICE_BUS)
        self.__eps = EPS()
        self.lowVoltage = 3.33 #Low Voltage


    def run(self, time):
        #send message to the arduino to power off the pi
        self.bus.write_byte_data(self.DEVICE_ADDR, self.RegisterADR, time)

    async def thresholdCheck(self):
        while True:
	    epsVoltage = self.__eps.getBusVoltage()
	    if epsVoltage < self.lowVoltage:
		    self.run(10) #1 hour
	    await asyncio.sleep(1) #check voltage every second
