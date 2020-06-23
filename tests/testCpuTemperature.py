import sys
sys.path.append('../')
from Drivers.cpuTemperature import CpuTemperature

cpu = CpuTemperature()
print(cpu.read())
