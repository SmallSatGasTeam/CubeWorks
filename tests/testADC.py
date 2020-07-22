import unittest
import sys
sys.path.append("../")

from Drivers.adc import ADC_Driver

class ADCTest(unittest.TestCase):
    adc = ADC_Driver.ADC()
    """
    A test case containing sets of assertions in the form of class methods.
    """
    def uvDark(self):
        """Asserts that the UV sensor reads < 0.2 volts when dark.  Assertion should pass when in dark"""
        self.assertTrue(adc.read(1) <= 0.2, "This should be true if dark")
    def sun1Dark(self):
        """Asserts that sun sensor 1 reads < 0.2 volts when dark.  Assertion should pass when in dark"""
        self.assertTrue(adc.read(5) <= 0.2, "This should be true if dark")
    def sun2Dark(self):
        """Asserts that sun sensor 2 reads < 0.2 volts when dark.  Assertion should pass when in dark"""
        self.assertTrue(adc.read(4) <= 0.2, "This should be true if dark")
    def sun3Dark(self):
        """Asserts that sun sensor 3 reads < 0.2 volts when dark.  Assertion should pass when in dark"""
        self.assertTrue(adc.read(2) <= 0.2, "This should be true if dark")
    def sun4Dark(self):
        """Asserts that sun sensor 4 reads < 0.2 volts when dark.  Assertion should pass when in dark"""
        self.assertTrue(adc.read(3) <= 0.2, "This should be true if dark")
    def sun5Dark(self):
        """Asserts that sun sensor 5 reads < 0.2 volts when dark.  Assertion should pass when in dark"""
        self.assertTrue(adc.read(0) <= 0.2, "This should be true if dark")
        
    def uvLight(self):
        """Asserts that the UV sensor reads > 3 volts when in uv light.  Assertion should pass when in uv light"""
        self.assertTrue(adc.read(1) >= 3, "This should be true if in uv light")
    def sun1Light(self):
        """Asserts that sun sensor 1 reads > 1 volts when in uv light.  Assertion should pass when in uv light"""
        self.assertTrue(adc.read(5) >= 1, "This should be true if in uv light")
    def sun2Light(self):
        """Asserts that sun sensor 2 reads > 1 volts when in uv light.  Assertion should pass when in uv light"""
        self.assertTrue(adc.read(4) >= 1, "This should be true if in uv light")
    def sun3Light(self):
        """Asserts that sun sensor 3 reads > 1 volts when in uv light.  Assertion should pass when in uv light"""
        self.assertTrue(adc.read(2) >= 1, "This should be true if in uv light")
    def sun4Light(self):
        """Asserts that sun sensor 4 reads > 1 volts when in uv light.  Assertion should pass when in uv light"""
        self.assertTrue(adc.read(3) >= 1, "This should be true if in uv light")
    def sun5Light(self):
        """Asserts that sun sensor 5 reads > 1 volts when in uv light.  Assertion should pass when in uv light"""
        self.assertTrue(adc.read(0) >= 1, "This should be true if in uv light")
    

    
#if __name__ == '__main__':
adc = ADC_Driver.ADC()
for i in range(0,6):
    print(adc.read(i))
    #unittest.main()
