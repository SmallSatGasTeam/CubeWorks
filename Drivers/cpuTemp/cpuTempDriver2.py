from Drivers.Driver import Driver
import os

class cpuTemp(Driver):
	def __init__(self):
		super().name = "cpuTemp"
	
	def read(self):
		temp = os.popen("vcgencmd measure_temp").readline()
<<<<<<< HEAD
		temp = float(temp.replace("temp="," ").replace("\'C"," ").replace("\n"," "))
		return temp

=======
        	temp = float(temp.replace("temp="," ").replace("\'C"," ").replace("\n"," "))
		temp = float(temp)
		return temp
>>>>>>> 7a1e12ca55bf6cd6d090f88e9c81e53f76a97796
	
