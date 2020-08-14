import numpy as np
import unittest
import sys
sys.path.append("../")
from Drivers.Magnetometer import Magnetometer

if __name__ == '__main__':
	mag = Magnetometer()
	print(mag.read())
	print(np.linalg.norm(mag.read()))
