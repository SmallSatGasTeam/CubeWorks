import unittest

import Drivers.uvDriver.uvDriver_AD7998 as UVOne
import Drivers.uvDriver.uvDriver_mcp3008 as UVTwo

class TestUV(unittest.TestCase):
    """
    Initializes a test case for the UV Sensors.  Inherits from unittest.TestCase.
    Defines methods that test the following:
    1. The AD7998 input.
    2. The MCP3008 input.
    """

    testUVOne = UVOne.uvSensor()

    def testADPower(self):
        # voltage: 4v
        self.assertEqual(self.testUVOne, True)
        # voltage: 3.3v
        self.assertAlmostEqual(self.testUVOne, 6.7915208)
        # voltage: 0v
        self.assertAlmostEqual(self.testUVOne, 0.0000000)
        # voltage: 2v
        self.assertAlmostEqual(self.testUVOne, 4.1160732)

