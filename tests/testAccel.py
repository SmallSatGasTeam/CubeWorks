import numpy as np
import unittest
import sys
sys.path.append("../")
from Drivers import Accelerometer


if __name__ == '__main__':
	accel = Accelerometer.Accelerometer()
	print(accel.read())
	print(np.linalg.norm(accel.read()))
