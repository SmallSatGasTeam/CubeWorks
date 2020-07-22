import sys
sys.path.append("../")

from Drivers.UV import UVDriver

class UVTest(unittest.TestCase):
    uv = UVDriver.UVDriver()
    """
    A test case containing sets of assertions in the form of class methods.
    """
    def uvDark(self):
        """Asserts that the UV sensor reads < 0.2 volts when dark.  Assertion should pass when in dark"""
        self.assertTrue(adc.read(1) <= 0.2, "This should be true if dark")
    def uvDark(self):
        """Asserts that the UV sensor reads > 3 volts when in uv light.  Assertion should pass when in uv light"""
        self.assertTrue(adc.read(1) >= 3, "This should be true if in uv light")

    
uv = UVDriver.UVDriver()
print(uv.read())
