from Drivers.adc.ADC_DriverII import ADC


class uvSensor(ADC):

    adcChannel = 1

    def __init__(self):
        super().__init__("uvSensor")

    def uvRead(self):
        voltage = super().read(self.adcChannel)

        return voltage

