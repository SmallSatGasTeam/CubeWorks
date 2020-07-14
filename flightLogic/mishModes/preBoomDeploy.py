import asyncio
from safe import safe
from getDriverData import *
import Drivers.eps.EPS as EPS

class preBoomMode:
	def __init__(self):
		self.thresholdVoltage = 5 #Threshold voltage to deploy AeroBoom. 
        self.criticalVoltage = 3.3 #Critical voltage, below this go to SAFE
		self.darkVoltage = 1 #Average voltage from solar panels that, if below this, indicates GASPACS is in darkness
		self.darkMinutes = 5 #How many minutes GASPACS must be on the dark side for before moving forward
		self.lightMinimumMinutes = 5 #Minimum amount of time GASPACS must be on light side of orbit before deploying
		self.lightMaximumMinutes = 60 #Maximum amount of time GASPACS may be on light side of orbit before deploying
	
	async def run(self):
		ttncData = TTNCData()
        attitudeData = AttitudeData()
		asyncio.run(ttncData.collectTTNCData(), attitudeData.collectAttitudeData())
        safeMode = safe()
		asyncio.run(safeMode.thresholdCheck()) #Check battery conditions, run safe mode if battery drops below safe level 
		eps = EPS() #creating EPS object  
		
		#Write average solar panel voltage to file
			
		
		
