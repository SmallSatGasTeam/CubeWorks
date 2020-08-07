ADC Driver:
--
Location: ../Drivers/adc/ADC_Driver.py

Functionality:
	The ADC Driver sets up a SPi communication route with the ADC. Through the ADC it can then get data from our five Sun Sensors and one UV sensor. After this connection is made one can gather data from these sensors by calling: ADC_Driver.ADC.read(channel). 
(see Sun Sensor Driver and UV Driver)
