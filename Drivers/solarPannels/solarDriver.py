#Not done or tested as of yet, I am doing more research on the panels to get some more info on them. This is just the ground work for now. 

import Adafruit_GPIO.SPI as SPI
import spidev
class solarPanel:
    def __init__(self)
        spi = spidev.SpiDev()
        
    #this func will return an array of the tempatures from the solar panels. (there will always be 2)
    def run_solar():
        temps = []
        temps.append(self.__getSolarTemp())
        temps.append(self.__getSolartemp2())
        return temps

    #this guys go and get the temp from the respective panales. 
    def __getSolarTemp():
        super().__init__("solarPanel")
        spi.open(0, 24)
        #not sure what bond rate or what command to send well try this for now
        spi.max_speed_hz = 1000000
        return spi.xfer(0x01)
        

    def __getSolartemp2():
        super().__init__("solarPanel")
        spi.open(0, 26)
        #not sure what bond rate or what command to send well try this for now
        spi.max_speed_hz = 1000000
        return spi.xfer(0x01)
        

#Notes: 
#       I also need to do the value convertion, that is if the temp sensors return a value that needs to be converted. 
