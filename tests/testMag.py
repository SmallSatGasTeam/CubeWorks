import unittest
import sys
sys.path.append("../")

from Drivers.Magnetometer import LSM303AGR

#class ADCTest(unittest.TestCase):
#    """
#    A test case containing sets of assertions in the form of class methods.
#    """
    #def testDivTwo(self):
    #    """Asserts that 4 / 2 == 2.  Assertion should pass"""
    #    self.assertEqual(divByTwo(4), 2)
    

    
#if __name__ == '__main__':
mag = LSM303AGR.Magnetometer()
print(mag.read())
    #unittest.main()