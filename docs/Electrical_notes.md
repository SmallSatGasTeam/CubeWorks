# Electrical notes on devices

## Magnetometer/Accelerometer
Pins:
| Name | GPIO number | Pin Number|
| --- | --- | --- |
| SDA | 2 | 3 |
| SCL | 3 | 5 |
| INT1 | 16 | 36 |
| DRDY | 18 | 12 |

The values for this will vary greatly depending on the orientation of the computer board.
 Expected readings are:
``` 
Acceleration (m/s^2): X=-1.606 Y=-0.650 Z=9.523
Magnetometer (micro-Teslas): X=19.182 Y=4.909 Z=-39.490
```
If lying flat, the Z values should be similar to those above.

## ADC
Pins:
| Name | GPIO number | Pin Number|
| --- | --- | --- |
| MISO | 9 | 21 |
| MOSI | 10 | 19 |
| SCLK | 11 | 23 |
| CS | 25 | 22 |
 
*CS is active low. Setting the pin low allows you to communicate with the ADC

Channels:
| Sensor | ADC channel |
| --- | --- |
| UV sensor | 1 |
| Sun sensor 1 | 5 |
| Sun sensor 2 | 4 |
| Sun sensor 3 | 2 |
| Sun sensor 4 | 3 |
| Sun sensor 5 | 0 |

*The channels are weird, but it made the traces on the board work out nicely.

### UV sensor
The UV sensor circuit is tuned to that any UV light will cause the circuit to max out at around 3.3V (3.29V in testing) 
This is converted by the ADC into a 12 bit binary number, with 0 as 0V and 4096 as 3.3V.
When the sensor is exposed to UV light, it should read around 3.3V.

### Sun sensors
The Sun sensors have almost the exact same circuit as the UV sensor, except that they are tuned so that the max amount of sunlight the sensor can read corresponds to just below 3.3V in the circuit.

## EPS
Command 1 will give the battery voltage from the EPS as a 12 bit number (0-4096).
Multiply this by 0.0023394775 to get the voltage.
The raw battery bus should read between 3.5 - 4.12 V

## Solar Panel Temperature Sensors
The accuracy of the Temperature sensors are:
| Condition | Error margin |
| --- | --- |
| -25°C to 85°C | ±1.5°C |
| -55°C to 125°C | ±2.0°C |
