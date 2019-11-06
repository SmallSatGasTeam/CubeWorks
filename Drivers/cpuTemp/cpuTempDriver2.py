from Drivers.Driver import Driver
import os

class cpuTemp(Driver):
	def __init__(self):
		super().name = "cpuTemp"
	
	def read(self):
		temp = os.popen("vcgencmd measure_temp").readline()
        	return (temp.replace("temp=",""))
	
