from Drivers.Driver import Driver
import os

class cpuTemp(Driver):
	def __init__(self):
		super().name = "cpuTemp"
	
	def read(self):
		temp = os.popen("vcgencmd measure_temp").readline()
		temp = float(temp.replace("temp="," ").replace("\'C"," ").replace("\n"," "))
		return temp
