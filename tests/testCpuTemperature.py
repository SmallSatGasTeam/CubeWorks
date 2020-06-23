import sys
sys.path.append('../')
from Drivers.cpuTemperature import CpuTemperature
from time import sleep

cpu = CpuTemperature()
while True:
    print(cpu.read())
    sleep(0.3)
