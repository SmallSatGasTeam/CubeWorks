# this still needs some work, but it is the basics
# Written by Nathan Gibbs

from time import time
from Drivers.eps.EPS import getBusVoltage # this might work depending on how and from where this is run. The other option is to hard code the file path

startTime = time() + 200 # assuming that transmission is 200 seconds from now for testing purposes. Will recive this from Presten's code.

transmissionWindow = 30 # assuming 30 seconds to transmit for testing purposes. Will recive this from Presten's code.


def check(startTime, transmissionWindow):

    currentVoltage = getBusVoltage() 

    timeToWindow = startTime - time()

    bytesToSend = transmissionWindow * 123 # transmission rate

    requiredVoltage = bytesToSend * 1234 # this is the required power to transmit a byte (needs correct value)

    expectedVoltage = currentVoltage - 1 * timeToWindow # current voltage - experimentally defined drain rate? Perhaps the maximum expected drain rate.

    rebootTime = -1 # default value if it does not need to reboot. Otherwise it will be in Unix time


    #import pdb; pdb.set_trace()


    if requiredVoltage > expectedVoltage:
        if timeToWindow < 3: # minutes 
            goForTransmission = False
        else:
            goForTransmission = True
            reboot = True
            rebootTime = startTime - 3 # minutes

    else:
        goForTransmission = True



    return goForTransmission, reboot, rebootTime 



check(startTime, transmissionWindow)
