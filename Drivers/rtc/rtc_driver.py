from Drivers.Driver import Driver
from datetime import datetime

class RTC(Driver):
    def __init__(self):
        """
        Initializes a simple driver that only reads the system clock.
        """
        super().__init__('rtc')


    def read(self):
        """
        Returns the UTC time in miliseconds since the Unix epoch.
        The integer returned should be 64 bits in size and be on the order of 1500000000000.
        """
        return int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * 1000)


