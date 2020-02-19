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
>> * Using the VOLTAGE_STEP constant, which is defined as ![voltage_step_equation](http://www.sciweavers.org/tex2img.php?eq=%5Cfrac%7BV_%7Bref%5C_in%7D%7D%7B4096%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)
## Implementation
## Testing
