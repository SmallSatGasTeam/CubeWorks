from Drivers.Driver import Driver
from os import popen

class CpuTemperature(Driver):
	def __init__(self):
		super().__init__(CpuTemperature)

	def read(self):
		temp = popen("vcgencmd measure_temp").readline()
		temp = float(temp.replace("temp="," ").replace("\'C"," ").replace("\n"," "))
		return temp

