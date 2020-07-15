import numpy as np
import unittest
import sys
sys.path.append("../")

from Drivers.Accelerometer import Accelerometer

class ADCTest(unittest.TestCase):
    accel = Accelerometer()
    """
    A test case containing sets of assertions in the form of class methods.
    """
    def testAccel(self):
        """Asserts that the magnitutde of the vector is between 9.5 and 10.1.  Assertion should pass"""
        self.assertTrue(np.linalg.norm(mag.read()) >= 9.5 && np.linalg.norm(mag.read()) <= 10.1)
    

    
#if __name__ == '__main__':
accel = Accelerometer()
    #unittest.main()
print(accel.read())
print(np.linalg.norm(accel.read()))
