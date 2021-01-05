import numpy as np
import unittest
import sys
from time import sleep
sys.path.append("../")
from Drivers.Magnetometer import Magnetometer

if __name__ == '__main__':
	mag = Magnetometer()
	print(mag.read())
	while True:
		print(np.linalg.norm(mag.read()))
		sleep(.25)
