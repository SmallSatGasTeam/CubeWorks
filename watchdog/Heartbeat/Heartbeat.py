import RPi.GPIO as GPIO
from time import sleep

# this is the heart beat code. objectives are:
# 1) A function that sends one pulse
#   A)


def setUp():

    GPIO.setwarnings(False)

    # Use physical pin numbering
    GPIO.setmode(GPIO.BOARD)

    # Set pin 7 to be an output pin and set initial value to low (off)
    GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)


# this function sends a single pulse
def singlePulse():
    waitTime = 1
    setUp()
    # wait a four seconds.
    sleep(waitTime)
    # send a pulse
    GPIO.output(7, GPIO.HIGH)
    sleep(0.00005)
    GPIO.output(7, GPIO.LOW)


def longTap():
    waitTime = 4
    setUp()
    while True:
        # send a pulse
        GPIO.output(7, GPIO.HIGH)
        sleep(0.00005)
        GPIO.output(7, GPIO.LOW)
        # wait a four seconds.
        sleep(waitTime)
