# Uploading notes
Sometimes the Arduino Beetle has an issue when uploading new code onto the board where the arduino IDE will be stuck in the "Uplodaing" section.
To fix this, go to file > preferances and select show verbose output during upload.
After the code is finished compiling, the upload terminal will display 
```
PORTS {COM7, } / {COM7, } => {}
PORTS {COM7, } / {COM7, } => {}
```
During this time, quicky reset the Arduino once or twice.
The reset timing can be finicky, so it may take a few tries.

# Resetting the Arduino
To reset the Arduino Beetle, turn the board over to the back side and there will be six pads, five circular, and one square, like the following:

(1)   (2)   [3]

(4)   (5)   (6)

Pads 1 and 4 should have white silkscreen in between them. Connect pins 1 and 4 to reset the Beetle.
