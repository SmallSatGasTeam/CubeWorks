from datetime import datetime
from math import sin, pi

from Drivers.Driver import Driver


class DummyMagnetometer(Driver):
    def __init__(self):
        super().__init__("DummyMagnetometer", 0.33)
        self.initial_time = datetime.now()

    def read(self):
        # Trying to simulate a slow spin, using a periodic function.
        # While spinning, the x and y axes should read between -1g and 1g.

        # f(x) = A*sin(Bx + C) -> A is the amplitude, 2π/B is the period, C is offset
        x = (datetime.now() - self.initial_time).seconds
        a = 1
        b = 1
        c = pi / 2

        # No acceleration in y axis, periodic acceleration in x, z axes.
        accel = (round(a * sin(b * x), 3), 0, round(a * sin(b * x + c), 3))
        return accel, (1, 1, 1)
