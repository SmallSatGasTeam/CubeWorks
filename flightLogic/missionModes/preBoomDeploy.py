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
		self.lightMaximumMinutes = 60 #Maximum amount of time GASPACS may be on light side of orbit before deploying, must be less than 90 by a fair margin since less than half of orbit can be sun
		self.batteryStatusOk = False
		self.maximumWaitTime = 240 #Max time GASPACS can wait, charging batteries, before SAFEing
		self.timeWaited = 0
		
	async def run(self):
	ttncData = TTNCData()
        attitudeData = AttitudeData()
	asyncio.run(ttncData.collectTTNCData(2), collectAttitudeData())#Pre-boom is mode 2
        safeMode = safe()
		asyncio.run(safeMode.thresholdCheck()) #Check battery conditions, run safe mode if battery drops below safe level 
		eps = EPS() #creating EPS object  
		sunlightData = []
		await while True: #Monitor the sunlight
			averageVoltage = (eps.getSPXVoltage()+eps.getSPYVoltage()+eps.getSPZVoltage())/3
			await asyncio.sleep(5)
			averageVoltage = (averageVoltage + (eps.getSPXVoltage()+eps.getSPYVoltage()+eps.getSPZVoltage())/3)/2
			await asyncio.sleep(5) #Every 10 seconds, record average solar panel voltage. Rough running average to avoid jumps in avg. voltage
			sunlightData.append(averageVoltage)
		
		await while True: #iterate through array, checking for set amount of dark minutes, then set amount of light minutes no greater than the maximum. When light minutes are greater than the maximum, empties array
			i=0
			darkLength = 0
			lastDark = 0
			while i < len(sunlightData): #Loop through sunlightData, checking for X minutes of darkness
				if(sunlightData[i]<self.darkVoltage):
					darkLength+=1 #It was in the dark for the 10 seconds recorded in the ith position of sunlightData
				else:
					darkLength = 0 #Maybe darkLength -=1 to avoid damage from one bad measurement? Maybe a smoother running average?
				if(darkLength>self.darkMinutes*6): #If GASPACS has been in dark longer than the preset amount
					lastDark = i
					break
				i+=1
			if lastDark != 0: #Condition from previous while loop has  been met
				q=lastDark
				lightLength = 0
				while q < len(sunlightData):
					if(sunlightData[q]>=self.darkVoltage):
						lightLength+=1
					else:
						lightLength = 0 #Maybe lightLength -=1 to avoid 1 bad measurement resetting everything
					if(lightLength>self.lightMaximumMinutes*6): #Has been in the light for too long
						sunlightData.clear() #Reset array of data
						break
					if(lightLength>self.lightMinimumMinutes*6 and batteryStatusOk=True):
						return True #Go on to Boom Deploy Mode if the battery is Ok
					q += 1
			await asyncio.sleep(15) #Run this whole while loop every 15 seconds
			
		await while True: #Checking the battery voltage to see if it's ready for deployment, if it is too low for too long --> SAFE
			if (eps.getBusVoltage()>self.thresholdVoltage):
				self.batteryStatusOk=True
            		else:
                		if(self.timeWaited*12 > self.maximumWaitTime): #5 seconds every wait
                    			safeMode.run(10) #1 hour
                		else:
                    			#Wait 1 minute
					self.timeWaited = self.timeWaited+1
                    			await asyncio.sleep(5) #Check battery every 5 seconds
				

			
		
		
