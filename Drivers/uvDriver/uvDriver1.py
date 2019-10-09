
#data arg should be a 12bit binary number as type string
def calculateIndex(data):
    #adc lsb found by Vrefin / 4096, 5V / 4096
    voltageStep = 0.001220703125
    #converts the 12 bit binary number to decimal
    numberOfSteps = int(data,2)
    #calculate the output voltage from UV sensor
    voltage = round(numberOfSteps * voltageStep,3)
    #turn voltage into photocurrent
    photoCurrent = round(voltage / 4.3 * 1000,4)
    #turn photocurrent into uv power
    uvPower = round(photoCurrent/113,3)
    return(uvPower)

