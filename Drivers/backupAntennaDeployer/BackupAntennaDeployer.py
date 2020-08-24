from Drivers.Driver import Driver
import asyncio
import RPi.GPIO as GPIO

class BackupAntennaDeployer(Driver):
    def __init__(self):
        """
        Calls parent constructor, sets burn time, sets GPIO pins
        """
        super().__init__("BackupAntennaDeployer")
        # Initial values
        self.burnTime = 10

        # Set up the GPIO pins for use
        GPIO.setmode(GPIO.BCM)

        # Setup GPIO pins
        # Primary Backup Pin: BOARD 33 which is GPIO 23
        self.primaryPin = 23
        # Secondary Backup Pin: BOARD 32 which is GPIO 26
        self.secondaryPin = 26
        GPIO.setup(self.primaryPin,GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.secondaryPin,GPIO.OUT, initial=GPIO.LOW)

    async def deployPrimary(self):
        """
        Set primary deploy pin to high for a specified time, triggering the
        backup antenna burn.
        """
        #Burn primary backup, then turn off and wait
        GPIO.output(self.primaryPin, GPIO.HIGH)
        await asyncio.sleep(self.burnTime)
        GPIO.output(self.primaryPin, GPIO.LOW)

    async def deploySecondary(self):
        """
        Set secondary deploy pin to high for a specified time, triggering the
        backup antenna burn.
        """
        GPIO.output(self.secondaryPin, GPIO.HIGH)
        await asyncio.sleep(self.burnTime)
        GPIO.output(self.secondaryPin, GPIO.LOW)

    def read(self):
        """
        Left undefined as no data is collected by this component
        """
        pass
