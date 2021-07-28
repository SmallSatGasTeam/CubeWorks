from Drivers.Driver import Driver
from time import sleep
from picamera import PiCamera
from os import listdir
#from os.path import expanduser
from os import makedirs
from os import system
from pathlib import Path
import subprocess

class Camera(Driver):
    def __init__(self):
        """
        Takes a picture
        """
        #super().__init__("Camera")

        self.highRes = (3280, 2464)
        self.lowRes = (640, 480)
        #self.pictureDirectoryPath = expanduser('~/Pictures')
        #self.pictureDirectoryPath = str(Path(__file__).parent / "../../Pictures")
        self.pictureDirectoryPath = "/home/pi/flightLogicData/Pictures"
        self.pictureNumber = 0
        try:
            self.__cam = PiCamera()
        except: 
            self.__cam = None

    def read(self):
        pass

    def takePicture(self):
        """
        Takes the picture
        """
        try :
            #the way to count folders in directory is len(os.listdir(path of directory to count in))
            #you have to import OS
            #This also counts files in the total, but with the file structure we came up with this shouldn't be a problem
            makedirs(self.pictureDirectoryPath, exist_ok=True)
            self.pictureNumber = len(listdir(self.pictureDirectoryPath))
            print("Picture number:", self.pictureNumber)
            #count number of folders in directory, add 1 for current pic

            self.__cam.resolution = self.lowRes
            print("Resolution:", self.__cam.resolution)
            sleep(2)
            makedirs(self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/LowRes", exist_ok=True)
            print("Made LowDir")
            self.__cam.capture(self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/LowRes/LowResOriginal"+str(self.pictureNumber)+".jpg")
            print("Captured Low")
            self.__cam.resolution = self.highRes
            print("Res:", self.__cam.resolution)
            makedirs(self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/HighRes", exist_ok=True)
            print("Made HighDir")
            self.__cam.capture(self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/HighRes/HighResOriginal"+str(self.pictureNumber)+".jpg")
            print("Took pictures")
            return self.pictureNumber
        except:
            #return neg 1 if no picture was taken
            print("Failed to take a picture")
            return -1

    def compressLowResToFiles(self, pictureNumber):
        """
        Compresses the Low Res to files. Compresses with SSDV, converts from Hex to ASCII with xxd, splits into 128 byte files.
        """
        self.pictureNumber = pictureNumber
        #Set up paths for low res picture and creates the packets directory
        lowResOriginalPath = self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/LowRes/LowResOriginal"+str(self.pictureNumber)+".jpg"
        lowResSSDVPath = self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/LowRes/LowResOriginal"+str(self.pictureNumber)+".bin"
        print("before compress")
        ssdv_lowRes_picture = system('sudo /home/pi/ssdv/ssdv -e -c N7GAS -i ' + str(pictureNumber) + " " + str(lowResOriginalPath) + ' ' + str(lowResSSDVPath))
        print("After compress")
    def compressHighResToFiles(self,pictureNumber):
        """
        Compresses the Low Res to files. Compresses with SSDV, converts from Hex to ASCII with xxd, splits into 128 byte files.
        """
        self.pictureNumber = int(pictureNumber)

        #Set up paths for high res picture and creates the packets directory
        highResOriginalPath = self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/HighRes/HighResOriginal"+str(self.pictureNumber)+".jpg"
        highResSSDVPath = self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/HighRes/HighResOriginal"+str(self.pictureNumber)+".bin"

        ssdv_highRes_picture = system('sudo /home/pi/ssdv/ssdv -e -c N7GAS -i ' + str(pictureNumber + 100) + " " + str(highResOriginalPath) + ' ' + str(highResSSDVPath))
