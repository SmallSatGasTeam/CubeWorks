from Drivers.adc.ADC_DriverII import ADC


class sunSensor(ADC):

    adcChannel = [5, 4, 2, 3, 0]
    voltageList = []

    def __init__(self):
        super().__init__("Sun Sensor")

    def uvRead(self):
        for i in range(0, 4):
            self.voltageList.append(super().read(i))

        return self.voltageList
