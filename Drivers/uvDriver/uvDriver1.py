
#data arg should be a 12bit binary number as type string
def calculateIndex(data):
    #adc lsb found by Vrefin / 4096 which is 5V / 4096
    voltageStep = 0.001220703125

    #converts the 12 bit binary number to decimal
    numberOfSteps = int(data,2)

    #calculate the output voltage from UV sensor
    voltage = numberOfSteps * voltageStep

    #calculate the uvPower
    #currentInNanoamps = Voltage / 4.3 * 1000
    #uvPower = current / 113
    uvPower = voltage * 1000 / 485.9
    return(uvPower)
