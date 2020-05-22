import unittest

import Drivers.camera.camera_driver as cam
from time import time
from math import trunc
import os.path

class TestCamera(unittest.TestCase):
    """
    Initializes a test case for the pi camera.  Inherits from unittest.TestCase.
    Defines methods that test the following:
    1. The initial file path is '/default/path'.
    2. The resolution of the camera should be 1024x1024.
    3. Takes a picture and asserts that a file exists where the picture was saved.
    """
    testCam = cam.Camera() # initialize camera

    def testCameraInitFilePath(self):
        """
        Asserts that the initial file path is '/default/path'.
        """
        self.assertEqual(self.testCam.latest_capture, "/default/path")

    def testCameraInitResolution(self):
        """
        Asserts that the camera resolution is set to 1024x1024 pixels.
        """
        self.assertEqual(self.testCam.camera.resolution, (1024, 1024))

    def testTakePicture(self):
        """
        Takes a picture and saves it to the file system.
        Asserts that there is a file where the picture was saved.
        """
        self.testCam.take_picture()
        self.assertTrue(os.path.isfile(self.testCam.latest_capture))
