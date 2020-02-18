from Drivers.Driver import Driver
import os

class cpuTemp(Driver):
	def __init__(self):
<<<<<<< HEAD
		super().__init__("cpuTemp")
=======
	    super().__init__("cpuTemp")
            #>>>>>>> d24cb1476aaaa15c935a4518c554f7caf8a1cd43
>>>>>>> d502766930ea27015c423609ee2cd2c397ddbf64
	
	def read(self):
		temp = os.popen("vcgencmd measure_temp").readline()
		temp = float(temp.replace("temp="," ").replace("\'C"," ").replace("\n"," "))
		return temp
