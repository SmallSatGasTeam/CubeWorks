from Drivers.Driver import Driver
from time import sleep
import RPi.GPIO as GPIO

class BoomDeployer(Driver):
    def __init__(self):
        """
        Calls parent constructor, Defines initial burn time, time to wait in between burns,
        and how many times to burn before giving up.  Sets up the GPIO pin for use by the actuate method.
        """
        super().__init__("Camera")
        # Initial values 
        self.burnTime = 4
        self.waitTime = 10
        self.numTimes = 3

        # Set up the GPIO 8 for use
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(8, GPIO.OUT, initial=GPIO.HIGH)


    def deploy(self):
        """
        Loop a specified number of times, turning off the GPIO pin to start the burn, 
        Wait for a specified amount of time, turn on the pin to end the burn, 
        wait again, and loop, increasing the burn time on each iteration
        """
        for num in range(0, self.numTimes):
            # Turn off begin burn
            GPIO.output(8, GPIO.LOW) 
            # Burn for burnTime + num seconds
            sleep(self.burnTime + num) 
            # Turn on end burn
            GPIO.output(8, GPIO.HIGH)
            # wait
            sleep(self.waitTime) 

    def read(self):
        """
        Left undefined as no data is collected by this component
        """
        pass


