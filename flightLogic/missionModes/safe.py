import sys
sys.path.append('../../')
import Drivers.eps.EPS as EPS
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
"HEY WERE NOT USING THIS RIGHT NOW" 
class safe:
	def __init__(self, saveObject):
		#Setup I2C bus for communication
		self.DEVICE_ADDR = 0x08
		self.bus = smbus.SMBus(1)
		self.__eps = EPS()
		self.thresholdVoltage = 3.33 #Threshold Voltage
		self.__saveObject = saveObject
		self.heartbeatTask = asyncio.create_task(self.heartBeat())
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM) #Physical Pin numbering
		GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW) #Sets pin 40 (GPIO 21) to be an output pin and sets the initial value to low (off)



	def run(self, time):
		#send message to the arduino to power off the pi
		#make sure we are not about to tx
		if(self.__saveObject is not None and self.__saveObject.checkTxWindow()):
			self.bus.write_byte(self.DEVICE_ADDR, time)
			self.heartbeatTask.cancel() #Cancel the heartbeat task
			print('Sent power-off command')
		else:
			self.bus.write_byte(self.DEVICE_ADDR, time)
			self.heartbeatTask.cancel() #Cancel the heartbeat task
			print('Send power-off command')

		sleep(15)
		print("killing heartbeat code")

	async def thresholdCheck(self):
		while True:
			epsVoltage = self.__eps.getBusVoltage()
			if epsVoltage < self.thresholdVoltage:
				print("Going into SAFE. eps voltage was  "+ str(epsVoltage))
				self.run(10)
				self.heartBeatTask.cancel()
			else:
				print('Threshold is good')
			await asyncio.sleep(1) #check voltage every second

	async def heartBeat(self): #Sets up up-and-down voltage on pin 40 (GPIO 21) for heartbeat with Arduino
		waitTime = 4
		while True:
			GPIO.output(21, GPIO.HIGH)
			print("Heartbeat wave high")
			await asyncio.sleep(waitTime/2)
			GPIO.output(21, GPIO.LOW)
			print("Heartbeat wave low")
			await asyncio.sleep(waitTime/2)
