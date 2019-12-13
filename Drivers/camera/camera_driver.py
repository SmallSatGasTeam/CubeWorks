from Drivers.Driver import Driver
from picamera import PiCamera
from os import getcwd
from time import time
from math import trunc

class Camera(Driver):
    def __init__(self):
        """
        Calls back to the parent (Driver)  constructor, initializes the latest_capture variable, 
        and initializes the camera hardware.  Note that use of the max resolution of the camera,
        2592 x 1944 pixels,  may crash the driver.
        """
        super().__init__("Camera")
        self.latest_capture = "/path/to/file"
        self.camera = PiCamera()
        self.camera.resolution = (1024, 1024) # Max (2592, 1944)

    def read(self):
        """Returns the filepath of the most recent picture taken."""
        return self.latest_capture

    def take_picture(self):
        """
        Sets the latests_capture variable to the filepath to a new file named for the current timestamp 
        (unix epoch) and uses that filepath to capture a new image.
        """
        self.latest_capture = getcwd() + "/Drivers/camera/captures/" + str(trunc(time())) + ".jpg"
        self.camera.capture(self.latest_capture)


