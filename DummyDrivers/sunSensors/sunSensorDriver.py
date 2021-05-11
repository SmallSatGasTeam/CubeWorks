from DummyDrivers.Driver import Driver
from DummyDrivers.adc import ADC_Driver
from datetime import datetime

class sunSensor(Driver):
    """
    This class calls the ADC driver and asks for data from the UV channel
    """
    #adc = ADC_Driver.ADC()
    #adcChannel = [5, 4, 2, 3, 0]
    #voltageList = []

    def __init__(self):
    #     super().__init__("Sun Sensor")
        self.voltageList=[] * 5

    def read(self):
    #     """
    #     This function calls the read function of the ADC for each channel a sun sensor has and return a list of the voltages
    #     """
    #     for i in range(0, 5):
    #         self.voltageList.append(51)

    #     return self.voltageList

        v = [0, 0, 0, 0, 0]
        self.voltageList = [0, 0, 0, 0, 0]
        getTime = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds())
        #Sun length is the amount of time the satellite will be in the sun
        sunLength = 1.1

        interval = sunLength*60
        switch = 20

        if ((getTime % interval) == 0) | ((getTime % interval) == switch):
            v[0] = 1.5
            v[4] = v[3] = v[2] = v[1] = v[0]
        elif (getTime % interval) > switch:
            v[4] = v[3] = v[2] = v[1] = v[0] = 3.3
        elif (getTime % interval) < switch:
            v[4] = v[3] = v[2] = v[1] = v[0] = 0.0

        self.voltageList = v

        print("Dummy sun sensor driver voltage list: ", self.voltageList, "Time, interval, switch: ", getTime%interval, interval, switch)

        return self.voltageList