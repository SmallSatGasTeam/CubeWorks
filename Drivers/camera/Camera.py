from Drivers.Driver import Driver
from time import sleep
from picamera import PiCamera
from os import listdir

class Camera(Driver):
    def __init__(self):
        """
        Takes a picture
        """
        super().__init__("Camera")

        self.highRes = (3280, 2464)
        self.lowRes = (640, 480)
        self.pictureDirectoryPath = "~/Pictures"

    def takePicture(self):
        """
        Takes the picture
        """
        #the way to count folders in directory is len(os.listdir(path of directory to count in))
        #you have to import OS
        #This also counts files in the total, but with the file structure we came up with this shouldn't be a problem
        pictureNumber = len(listdir(self.pictureDirectoryPath)+1 #count number of folders in directory, add 1 for current pic #
        camera = PiCamera()
        camera.resolution = self.lowRes
        sleep(2)
        camera.capture(self.pictureDirectoryPath+"/"+str(pictureNumber)+"/LowRes/'LowResOriginal.jpg'")
        camera.resolution = self.highRes
        camera.capture(self.pictureDirectoryPath+"/"+str(pictureNumber)+"/HighRes/'HighResOriginal.jpg'")

    def compress(self):
        """
        Compresses the image using SSDV
        """

