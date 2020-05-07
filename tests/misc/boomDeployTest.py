import RPi.GPIO as GPIO
from time import sleep

burnTime = 4
waitTime = 10
numTimes = 3

GPIO.setwarnings(False)

# Use physical pin numbering
GPIO.setmode(GPIO.BOARD) 

# Set pin 8 to be an output pin and set initial value to high (on)
GPIO.setup(8, GPIO.OUT, initial=GPIO.HIGH) 

# wait 60 seconds before start
sleep(60)

for num in range(0, numTimes):
    # Turn off begin burn
    GPIO.output(8, GPIO.LOW) 
    # Burn for burnTime + num seconds
    sleep(burnTime + num) 
    # Turn on end burn
    GPIO.output(8, GPIO.HIGH)
    # wait
    sleep(waitTime) 
