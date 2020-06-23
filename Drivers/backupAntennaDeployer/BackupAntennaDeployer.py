from Drivers.Driver import Driver
from time import sleep
import RPi.GPIO as GPIO

class BackupAntennaDeployer(Driver):
    def __init__(self):
        """
        Calls parent constructor, sets burn time, sets GPIO pins
        """
        super().__init__("BackupAntennaDeployer")
        # Initial values
        self.burnTime = 10
        self.waitTime = 5

        # Set up the GPIO pins for use
        GPIO.setmode(GPIO.BOARD)

        #Setup GPIO pins
        self.primaryPin = 32
        self.secondaryPin = 33
        GPIO.setup(self.primaryPin,GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.secondaryPin,GPIO.OUT, initial=GPIO.LOW)

    def deploy(self):
        """
        Consecutively set primary and then secondary antenna deploy pins to high
        for a specified amount of time
        """
        #Burn primary backup, then turn off and wait
        GPIO.output(self.primaryPin, GPIO.HIGH)
        sleep(self.burnTime)
        GPIO.output(self.primaryPin, GPIO.LOW)
        sleep(self.waitTime)

        #Burn secondary backup, then turn off and cleanup
        GPIO.output(self.secondaryPin, GPIO.HIGH)
        sleep(self.burnTime)
        GPIO.output(self.secondaryPin, GPIO.LOW)

        GPIO.cleanup()
    def read(self):
        """
        Left undefined as no data is collected by this component
        """
        pass
