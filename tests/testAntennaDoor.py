import sys
sys.path.append('../')
from Drivers.antennaDoor import AntennaDoor
from time import sleep

antennaDoor = AntennaDoor()
while True:
    print(antennaDoor.readDoorStatus())
    sleep(1)
    antennaDoor.deployAntennaMain()
    sleep(1)

