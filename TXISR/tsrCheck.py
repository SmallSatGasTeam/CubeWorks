# this still needs some work, but it is the basics


from time import time
from Drivers.esp.ESPdriver import getBusVoltage

currentVoltage = getBusVoltage() 

transmissionTime = time() + 200 # assuming that transmition is 200 seconds from now

transmissionWindow = 30 # assuming 30 seconds to transmit

timeToWindow = transmissionTime - time()

bytesToSend = transmissionWindow * 123 # transmissionRate

requiredVoltage = bytesToSend * 1234 # this is the required power to transmit a byte (needs correct value)

expectedVoltage = currentVoltage - 1 * timeToWindow # currentVoltage - experimentaly defined drain rate


#import pdb; pdb.set_trace()


if requiredVoltage > expectedVoltage:
    if timeToWindow < 3: # minutes 
        goForTransmission = False
    else:
        goForTransmission = True
        reboot = True
        rebootTime = transmissionTime - 3 # minutes

else:
    goForTransmission = True

print("go for transmission: ", goForTransmission)
print("reboot: ", reboot)
if reboot == True:
    print("reboot time: ", rebootTime)
