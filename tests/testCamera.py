import sys
sys.path.append('../')
from Drivers.camera import Camera
cameraObject = Camera()
cameraObject.takePicture()
#cameraObject.compressLowResToFiles(19)
#print("Low Res Done")
#cameraObject.compressHighResToFiles(18)
#print("High Res Done")
