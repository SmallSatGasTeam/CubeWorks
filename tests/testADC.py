import unittest
import sys
sys.path.append("../")

from Drivers.adc import ADC_Driver

#class ADCTest(unittest.TestCase):
#    """
#    A test case containing sets of assertions in the form of class methods.
#    """
    #def testDivTwo(self):
    #    """Asserts that 4 / 2 == 2.  Assertion should pass"""
    #    self.assertEqual(divByTwo(4), 2)
    

    
#if __name__ == '__main__':
adc = ADC_Driver.ADC()
print(adc.read(1))
    #unittest.main()
