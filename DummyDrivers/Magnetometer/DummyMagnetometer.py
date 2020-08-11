from DummyDrivers.Driver import Driver
from datetime import datetime

class DummyMagnetometer(Driver):
    def __init__(self):
        super().__init__("DummyMagnetometer", 0.33)
        self.initial_time = datetime.now()

    def read(self):
        return 22,23,24
