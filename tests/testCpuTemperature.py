import sys
sys.path.append('../')
from Drivers.cpuTemperature import CpuTemperature
from time import sleep

cpu = CpuTemperature()
for i in range(0,10):
    print(cpu.read())
    sleep(1)
print("Removing the delay to pin the CPU, temperature should increase")
for i in range(0,300):
    print(cpu.read())
print("Added the delay back, temperature should decrease")
for i in range(0,10):
    print(cpu.read())
    sleep(1)
