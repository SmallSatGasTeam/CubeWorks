### This test activates the primary antenna deployment system over I2C using Algorithm 2 ###
import sys
sys.path.append('../')
from Drivers.antennaDoor import AntennaDoor
from time import sleep

antennaDoor = AntennaDoor()
print("WARNING THIS WILL DEPLOY THE ANTENNA!!!!") 
for i in range(10):
    print("Count down: ", 10 - i)
while True:
    print(antennaDoor.readDoorStatus())
    sleep(1)
    antennaDoor.deployAntennaMain()
    sleep(1)
