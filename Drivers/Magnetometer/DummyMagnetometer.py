from Drivers.Driver import Driver


class DummyMagnetometer(Driver):
    def __init__(self):
        super().__init__('DummyMagnetometer', 1)

    def read(self):
        return (1, 1, 1), (1, 1, 1)
