#code to read input from GPIO pin and tell us it it is open or closed.

import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

run_once1 = 1
DEBUG = 1

while True:
    if run_once1 == 1:
        if GPIO.input(27) == 1:
            run_once1 = 0
            print("27")

