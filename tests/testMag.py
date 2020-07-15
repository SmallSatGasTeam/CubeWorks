import numpy as np
import unittest
import sys
sys.path.append("../")

from Drivers.Magnetometer import Magnetometer

class ADCTest(unittest.TestCase):
    mag = Magnetometer()
    """
    A test case containing sets of assertions in the form of class methods.
    """
    def testMag(self):
        """Asserts that the magnitutde of the vector is between 64 and 66.  Assertion should pass"""
        self.assertTrue(np.linalg.norm(mag.read()) >= 64 && np.linalg.norm(mag.read()) <= 66)
    

    
#if __name__ == '__main__':
mag = Magnetometer()
print(mag.read())
print(np.linalg.norm(mag.read()))
    #unittest.main()
