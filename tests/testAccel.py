import numpy as np
import unittest
import sys
from time import sleep
sys.path.append("../")
from Drivers import Accelerometer


if __name__ == '__main__':
	accel = Accelerometer()
	print(accel.read())
	while True:
		print(np.linalg.norm(accel.read()))
		sleep(.25)
