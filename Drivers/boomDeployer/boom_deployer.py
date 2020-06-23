from Drivers.Driver import Driver
from time import sleep
import RPi.GPIO as GPIO

class BoomDeployer(Driver):
    def __init__(self):
        """
        Calls parent constructor, Defines initial burn time, time to wait in between burns,
        and how many times to burn before giving up.  Sets up the GPIO pin for use by the actuate method.
        """
        super().__init__("BoomDeployer")
        # Initial values
        self.burnTime = 4
        self.waitTime = 10
        self.numTimes = 3

        # Set up the GPIO 8 for use
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

	#First Wirecutter
	self.wireCutter1_high1 = 36
	self.wireCutter1_high2 = 38
	self.wireCutter1_low1 = 7
        GPIO.setup(self.wireCutter1_high1, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(self.wireCutter1_high2,GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(self.wireCutter1_low1,GPIO.OUT, initial=GPIO.HIGH)

	#Second Wirecutter
	self.wireCutter2_high1 = 35
	self.wireCutter2_high2 = 37
	self.wireCutter2_low1 = 29
        GPIO.setup(self.wireCutter2_high1, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(self.wireCutter2_high2,GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(self.wireCutter2_low1,GPIO.OUT, initial=GPIO.HIGH)


    def deploy(self):
        """
        Loop a specified number of times, setting the correct GPIO pins to HIGH/LOW  to start/stop
	the burn. Wait and then repeat with the other wirecutter mechanism
        """
        for num in range(0, self.numTimes):
	    #Turn on Wire Cutter 1
            GPIO.output(self.wireCutter1_high1, GPIO.HIGH)
            GPIO.output(self.wireCutter1_high2, GPIO.HIGH)
            GPIO.output(self.wireCutter1_low1, GPIO.LOW)
	    #Burn for set number of seconds
	    sleep(self.burnTime)
	    #Turn off Wire Cutter 1
	    GPIO.output(self.wireCutter1_high1, GPIO.LOW)
            GPIO.output(self.wireCutter1_high2, GPIO.LOW)
            GPIO.output(self.wireCutter1_low1, GPIO.HIGH)
	    #Wait
	    sleep(self.waitTime)


	    #Turn on Wire Cutter 2
            GPIO.output(self.wireCutter2_high1, GPIO.HIGH)
            GPIO.output(self.wireCutter2_high2, GPIO.HIGH)
            GPIO.output(self.wireCutter2_low1, GPIO.LOW)
	    #Burn for set number of seconds
	    sleep(self.burnTime)
	    #Turn off Wire Cutter 2
	    GPIO.output(self.wireCutter2_high1, GPIO.LOW)
            GPIO.output(self.wireCutter2_high2, GPIO.LOW)
            GPIO.output(self.wireCutter2_low1, GPIO.HIGH)
	    #Wait
	    sleep(self.waitTime)
	GPIO.cleanup()
    def read(self):
        """
        Left undefined as no data is collected by this component
        """
        pass


