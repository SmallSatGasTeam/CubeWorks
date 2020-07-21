import smbus
import Drivers.eps.EPS as EPS
import asyncio
#####################################################################################
#All this class does is tell the adruino to shut off the pi for the spesified amout 
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
    def __initi__(self, saveObject):
        #Setup I2C bus for communication
        self.DEVICE_BUS = 1
        self.__beetle = 0x08
        self.RegisterADR = 0x00
        self.bus = smbus.SMBus(self.DEVICE_BUS)
        eps = EPS()
        self.thresholdVoltage = 3.33 #Threshold Voltage
        


    def run(self, time):
        #send message to the adruino to power off the pi
        #make sure we are not about to tx 
        if(saveObject.checkTxWindow())self.bus.write_byte_data(self.DEVICE_ADDR, self.RegisterADR, time)
        
    async def thresholdCheck(self):
        await while True:
		epsVoltage = eps.getBusVoltage()
		if epsVoltage < self.thresholdVoltage:
			run(10) #1 hour
		await asyncio.sleep(1) #check voltage every second    
        
        
