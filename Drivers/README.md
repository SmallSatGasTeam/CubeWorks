GASPACS Software:The Drivers
===
Opening Note:
--
The purpose of the Drivers is to communicate between the Pi and the various sensors and components of the GASPACS mission.

The following drivers return sensor data:
- Accelerometer
- Magnetometer
- UV
- adc
- antennaDoor
- cpuTemperature
- rtc
- solarPanelTemp
- sunSensors

The following drivers are designed to configure, command, or control components:
- backupAntennaDeployer
- boomDeployer

The following drivers both configure components and return their values.
- camera
- transceiverConfig
- eps

All these drivers inherit from a single file called Driver.py. Their relationship with this file gives them the ability to run asynchronously as well as making the code more organized and easier to handle. For more documentation on each driver, there is a readme located in each Driver folder. 

