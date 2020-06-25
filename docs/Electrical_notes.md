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
The EPS module is connected on the I2C bus, with a seperate pin for an EPS reset.

Pins:
| Name | GPIO number | Pin Number|
| --- | --- | --- |
| SDA | 2 | 3 |
| SCL | 3 | 5 |
| EPS_RST | 6 | 31 |

*EPS_RST is active low, setting the pin low will reset the EPS

Command 1 will give the battery voltage from the EPS as a 12 bit number (0-4096).
Multiply this by 0.0023394775 to get the voltage.
The raw battery bus should read between 3.5 - 4.12 V

## Solar Panel Temperature Sensors
The solar panels are connected to the Pi on the SPI bus.

Pins:
| Name | GPIO number | Pin Number|
| --- | --- | --- |
| MISO | 9 | 21 |
| MOSI | 10 | 19 |
| SCLK | 11 | 23 |
| Panel_1_Temp_CS | 7 | 26 |
| Panel_2_Temp_CS | 8 | 24 |

The accuracy of the Temperature sensors are:
| Condition | Error margin |
| --- | --- |
| -25°C to 85°C | ±1.5°C |
| -55°C to 125°C | ±2.0°C |

## Chronodot
The chronodot is connected to the Pi on the I2C bus, along with a reset pin, an interrupt, and a 32kHz square wave

Pins:
| Name | GPIO number | Pin Number|
| --- | --- | --- |
| SDA | 2 | 3 |
| SCL | 3 | 5 |
| RST | 22 | 15 |
| INT | 23 | 16 |
| 32kHz | 27 | 13 |

*The RST pin is active low, setting the RST pin low will cause the chronodot to reset

*The INT pin is also active low. 

The RST pin acts as both an external reset button, but also an internal reset indicator. The RST pin will go low if the suply voltage for the chronodot goes too low and the chronodot resets. This can indicate a comprimised clock.

The INT pin acts like an alarm. A specific time can be set, and at that time, the chronodot will set the INT pin low. Otherwise this pin is high.

The accuracy of the clock is ±2 minutes/year of operation 

## Wire cutters
The wire cutters have an on switch as two inhibits. 

Pins:
| Name | GPIO number | Pin Number|
| --- | --- | --- |
| WC1_on | 4 | 7 |
| WC1_safety1 | 20 | 38 |
| WC1_safety2 | 16 | 36 |
| WC2_on | 5 | 29 |
| WC2_safety1 | 26 | 37 |
| WC2_safety2 | 19 | 35 |

The inhibits must be set High and the on pin must be set Low to turn the wire cutters on.
