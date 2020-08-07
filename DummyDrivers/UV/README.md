UV Driver:
--
Location: ../Drivers/UV/UVDriver.py

Functionality:
	The UV Driver inherits functionality from the ADC Driver, much like the Sun Sensor Driver. It reads from a specific channel through the SPi connection created in the ADC Driver, and returns a single value. To get the data returned by this driver call UVDriver.UVDriver.read()
	

# UV Sensor Documentation
## Requirements
The the value of uv power hitting the uv sensor and return the power in mW/cm^2
## Design
> MCP3008  ADC
>> * The adc driver for the MCP3008 ADC returns a list with values in volts
>> * The uv sensor driver calls a method from the adc class, and gets the value in the uv sensor spot
>> * Using the formula given by the graphs on the GUVA-S12D uv sensor datasheet( uvPower = voltage * 1000 / 485.9), plug in the value returned by the adc and return uvPower as a float  

> AD7998 ADC
>> As of right now, the AD7998 ADC driver has not been written.  
Reading the datasheet tells us that the ADC will return a 12bit binary number over the I<sup>2</sup>C interface.  
As of now, assuming that the adc driver method call for the AD7998 adc returns a 12bit binary number, the design is as follows.  
>> * Using the VOLTAGE_STEP constant, which is defined as  <sup>V<sub>ref_in</sub></sup> / <sub>4096</sub> 
>> * 4096 come from the maximum decimal value able to be represented from 12bit binary
>> * The 12 bit binary number returned from the adc will be multiplied with the VOLTAGE_STEP constant to get the voltage
>> * This voltage is then plugged into the previous equation stated, uvPower = voltage * 1000 / 485.9
## Implementation
* import the adc class from the adc driver
* create an adc object
* call the read method specifying which register to return
* take the return value and depending on which adc it is dealing with, follow the steps outlined above
## Testing
> Testing with the MCP3008 ADC
>> * Running the ADC code seperatley gives a list of register values
>> * Running the uv sensor code returns the same value as the register in the 4th position

> Testing with the AD7998