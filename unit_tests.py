#################################################
# GASPACS Unit Tests
# Run with "python3 unit_tests.py --verbose"
#################################################

# Imports here
import unittest

# Camera Test imports
import Drivers.camera.camera_driver as cam
from time import time
from math import trunc
import os.path

################################################################
# Unit Test Class
#
# Each method in the class is one test case.  
# If there are multiple assertions in one method and one fails,
# the following one assertions will not be run
################################################################
class UnitTests(unittest.TestCase):
    # Initialize Components to test
    testCam = cam.Camera() # initialize camera


    ###########################################
    # Camera Tests
    ###########################################
    def testCameraInitFilePath(self):
        # Test the initial file path 
        self.assertEqual(self.testCam.latest_capture, "/path/to/file")

    def testCameraInitResolution(self):
        # Test the initial camera resolution
        self.assertEqual(self.testCam.camera.resolution, (1024, 1024))

    def testTakePicture(self):
        filename = str(trunc(time())) + '.jpg'
        self.testCam.take_picture()
        print(self.testCam.latest_capture)
        self.assertTrue(os.path.isfile(self.testCam.latest_capture))

        
################################################
# Main entry point. Don't write code after this.
################################################
if __name__ == '__main__':
    unittest.main()
