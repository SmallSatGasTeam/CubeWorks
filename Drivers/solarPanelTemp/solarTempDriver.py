from Drivers.adc.ADC_DriverII import ADC


class solarTemp(ADC):

    adcChannel = [5, 4, 2, 3, 0]
    adcReadingsInV = []

    def __init__(self):
        super().__init__("uvSensor")

    def solarRead(self):
        for i in range(5):
            self.adcReadingsInV.append(super().read(self.adcChannel[i]))
        return self.adcReadingsInV
