import sys
sys.path.append('../')
from Drivers.camera import Camera
cameraObject = Camera()
cameraObject.takePicture()

cameraObject.compressLowResToFiles(0)
print("Low Res Done")
cameraObject.compressHighResToFiles(0)
print("High Res Done")
