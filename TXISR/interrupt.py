# Inturrupt requires Pin
from machine import Pin

#import rxHandling.py
import rxHandling

def watchReceptions(btn):
    ## I think this is how this works...
    if btn.value() >= 1.5
       x = rxHandling.rxHandling()


# Part of inturrupt method 1:
#TODO: get the correct pin for the radio connection. 1.5-1.8 voltage
btn = Pin(0, Pin.IN)

# Create inturrupt
btn.irq(watchReceptions(btn))