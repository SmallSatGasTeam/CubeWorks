import sys
sys.path.append('../../')
import DummyDrivers.eps.EPS as EPS
import asyncio
import RPi.GPIO as GPIO
from os import system
from time import sleep
import smbus
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
	def __init__(self, saveObject):
		#Setup I2C bus for communication
		self.DEVICE_ADDR = 0x08
		self.bus = smbus.SMBus(1)
		self.__eps = EPS()
		self.thresholdVoltage = 3.33 #Threshold Voltage
		self.__saveObject = saveObject
		#GPIO.setwarnings(False)
		#GPIO.setmode(GPIO.BOARD) #Physical Pin numbering NOTE: 8/14/20, this threw an error 
		#GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW) #Sets pin 40 to be an output pin and sets the initial value to low (off)



	def run(self, time):
		#send message to the arduino to power off the pi
		#make sure we are not about to tx
		if(self.__saveObject is not None and self.__saveObject.checkTxWindow()):
			#self.bus.write_byte(self.DEVICE_ADDR, time)
			print('Sent power-off command')
		else:
			#self.bus.write_byte(self.DEVICE_ADDR, time)
			print('Send power-off command')

		sleep(15) #If Pi hasn't turned off by now, must take drastic measures. Kill heartbeat code!
		#system('pkill -9 python')
		print("killing heartbeat code")
		
	async def thresholdCheck(self):
		while True:
			epsVoltage = self.__eps.getBusVoltage()
			if epsVoltage < self.thresholdVoltage:
				print("Going into SAFE. eps voltage was  "+ str(epsVoltage))
				#self.run(10) #1 hour
			else:
				print('Threshold is good')
			await asyncio.sleep(1) #check voltage every second

	async def heartBeat(self): #Sets up up-and-down voltage on pin 40 for heartbeat with Arduino
		waitTime = 4
		while True:
			#GPIO.output(40, GPIO.HIGH)
			print("Heartbeat wave high")
			await asyncio.sleep(waitTime/2)
			#GPIO.output(40, GPIO.LOW)
			print("Heartbeat wave low")
			await asyncio.sleep(waitTime/2)
