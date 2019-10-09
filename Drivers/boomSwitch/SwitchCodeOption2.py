#code to indicate if detector switch is on or off.

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

while True:
GPIO.wait_for_edge(27, GPIO.RISING)
print(“Button 1 Pressed”)
GPIO.wait_for_edge(27, GPIO.FALLING)
print(“Button 1 Released”)

GPIO.cleanup()