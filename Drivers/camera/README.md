# Camera Documentation
## Introduction
This driver interfaces with a standard Raspberry Pi camera.  The The Raspberry Pi foundation maintains a robust Python 3 module for using the camera called `picamera`.  The maximum resolution that the Raspberry Pi camera can generate is 2592 x 1944 pixels (though approaching the max can result in errors).  The resolution that the driver takes pictures at is 1024 x 1024 pixels.  

## Requirements
1. Take a picture on command
	- Store the picture to the OS file system
	- Set the components latest image to the file path to the most recently taken picture
2. Return the most recently taken image's file path on command

## Dependencies
The following are Python 3 moduls that are required for the camera driver to run:
1. `Driver` (maintained by the GAS team)
2. `picamera`
3. `os`
4. `time`
5. `math`

## Implementation
### The Camera class and constructor
The `Camera` class inherits from the `Driver` class.  In the constructor, the parent `Driver` class constructor is called.  The constructor then initializes the following values:
1. `self.latest_capture = '/default/path'`
	- This is the value that refers to the most recently taken photo and its location on the system file tree.  
	- `/default/path` is a dummy value that is changed immediately after a new picture is taken 
2. `self.caera = PiCamera()`
	- This initializes a `PiCamera` object that uses the `picamera` api to take pictures
3. `self.camera.resolution = (1024, 1024)`
	- This sets the `PiCamera` objects resolution to 1024 x 1024 pixels

### The read method
The `read()` method is a class function that simply returns the `self.latest_capture` maintained by the `Camera` object.  

### The take_picture method
The `take_picture()` method is a class function that does x things:
1. Gets the current working directory of the python process using `os.getcwd()` 
2. Queries the system clock for the current time usiing `time.time()` and `math.trunc()` to truncate the time to an integer value
3. Assigns the `self.latest_capture` value to the current working directory, a hard coded relative path, the time, and the `.jpg` file extension appended together
4. Calls `camera.capture()` in the camera API, giving it `self.latest_capture` as the location to save the new image file

## Testing
The `Camera` module was tested using the test cases defined in `unit_tests.py` at the root of this repository.  The test follows the following procedure:
1. `testCameraInitFilePath()`
	- Asserts that the default file path is `/default/path`
		- The test fails if this assertion fails
	- This implies that the startup behavior of this value is stable and predictable
2. `testCameraInitResolution()`
	- Asserts that the resolution of the camera is set to the tuple `(1024, 1024)`
		- The test fails if this assertion fails	
3. `testTakePicture()`
	- Calls the `take_picture` method on the `Camera` class
	- Asserts that there is a file at `self.latest_capture` on the system file tree
		- The test fails if this assertion fails
		- This is the best we can do to test the picture without using computer vision to analyze the picture.  

These tests were run on February 25, 2020 and all passed with the following ouptut:
```
testCameraInitFilePath (__main__.UnitTests) ... ok
testCameraInitResolution (__main__.UnitTests) ... ok
testTakePicture (__main__.UnitTests) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.614s

OK
```
