GASPACS Software:The Drivers
===
Opening Note:
--
All these drivers inherit from a single file called Driver.py. Their relationship with this file gives them the ability to run asynchronously as well as making the code more organized and easier to handle.  


Accelerometer Driver 
--
Location: ../Drivers/Accelerometer/Accelerometer.py

Functionality: 
The Accelerometer Driver sets up an I2C communication route to the Accelerometer. After this connection is made it can gather the acceleration data by calling: Accelerometer.Accelerometer.read()


ADC Driver:
--
Location: ../Drivers/adc/ADC_Driver.py

Functionality:
	The ADC Driver sets up a SPi communication route with the ADC. Through the ADC it can then get data from our five Sun Sensors and one UV sensor. After this connection is made one can gather data from these sensors by calling: ADC_Driver.ADC.read(channel). 
(see Sun Sensor Driver and UV Driver)


Antenna Door Driver:
--
Location:  ../Drivers/antennaDoor/AntennaDoor.py

Functionality:
	The Antenna Door Driver sets up an I2C communication route with the Antenna Doors. After this connection is established the Driver is then able to determine whether the doors have or have not opened in order to confirm antenna deployment. The data collected may be acquired by calling: AntennaDoor.AntennaDoor.readDoorStatus()



Backup Antenna Deployment Driver:
--
Location:  ../Drivers/backupAntennaDeployerBackupAntennaDeployer.py

Functionality: 
	The Backup Antenna Deployment Driver sets up a connection to various pins. These pins are connected to capacitors that power the Antenna Doors. Through this connection the software will set the capacitors to turn on and open the Antenna Doors. This code will be used as a fail safe if the premade software to open the Antenna Doors is unsuccessful. The Antenna can be manually deployed by calling: BackupAntennaDeployer.BackupAntennaDeployer.deploy().


Boom Deployer Driver:
--
Location: ../Drivers/boomDeployer/BoomDeployer.py

Functionality:
	Our AeroBoom is stored in a container held shut by wire. The Boom Deployer Driver will set up a connection to various pins. These pins will be connected to both the wire cutters. After this connection is made the Driver will tell the first wire cutter to turn on for three seconds and then turn off. It will do this twice. Since there is no way for us to tell if the first wire cutter was successful we will then turn on the second wire cutter and run it in the same manner. This ensures that the AeroBoom gets deployed. The AeroBoom gets deployed by calling: boomDeployer.BoomDeployer.deploy()


Camera Driver:
--
Location: ../Drivers/camera/Camera.py

Functionality:
	The Camera Driver will take a photo and store the photo in a specific file with a very specific file path. This Driver will also give us the ability to compress the file into two different resolutions. In order to take a picture call Camera.Camera.takePicture(). In order to store the photo in either of the two resolutions call Camera.Camera.compressLowResToFiles(pictureNumber) 
Camera.Camera.compressHighResToFiles(pictureNumber) 

CPU Temperature Driver:
--
Location: ../Drivers/cpuTemperature/CpuTemperature.py

Functionality:
	The CPU Temperature Driver reads in the temperature of the CPU from the temperature sensor connected to the CPU. To collect the data gathered call CpuTemperature.CpuTemperature.read().


EPS Driver:
--
Location: ../Drivers/eps/EPS.py

Functionality:
	The EPS Driver sets up an I2C communication line with the EPS. Once this connection is established the Driver gains access to many different forms of data collected by the EPS. These data forms are: 

Cell temperature

MCU temperature

Bus voltage

Bus current

BCR Voltage

BCR current

3V3 current

5V current

SPX voltage

SPX minus current

SPX plus current

SPY voltage 

SPY minus current

SPY plus current

SPZ current

Magnetometer Driver:
--
Location: ../Drivers/Magnetometer/Magnetometer.py

Functionality:
	The Magnetometer Driver establishes an I2C connection with the Magnetometer. Once that connection is made the driver will then collect information concerning the direction, strength, or relative change of magnetic fields in relation to the satellite that have been gathered by the Magnetometer. To gain access to this information call Magnetometer.Magnetometer.read()


RTC Driver:
--
Location: ../Drivers/rtc/rtc_driver.py

Functionality:
	The RTC Driver is perhaps the most simple driver. All it does is read the system clock and return the value found there.This value will be the time in milliseconds since the Unix Epoch To get that value call: rtc_driver.RTC.read().





Solar Panel Temperature Driver:
--
Location: ../Drivers/solarPanelTemp/solarDriver.py

Functionality:
	The Solar Panel Temperature Driver establishes an SPi connection through the ADC to the two Temperature Sensors connected to the solar panels. After the connection is established this driver can return the temperature of the solar panels. In order to gain access to this data call: solarDriver.TempSensor.read().
	

Sun Sensor Driver:
--
Location: ../Drivers/sunSensors/sunSensorDriver.py

Functionality:
	The Sun Sensor Driver uses the ADC Drivers already established SPi connection. (See ADC Driver) Using polymorphism this driver reads in from multiple channels of communication via the ADC’s read() function. These channels are connected to the five Sun Sensors. The data collected from these sensors can be accessed by calling: sunSensorDriver.SunSensor.read() 


Transceiver Configuration Driver:
--
Location: ../Drivers/tranceiverConfig/TranceiverConfig.py

Functionality:
	The Transceiver Configuration Driver does not handle the transmissions. It does, however, turn on and off the beacon, turn on low power mode, and read the internal temperature sensor. To access these different capabilities see the following commands:
Turn off the beacon: TranceiverConfig.TranceiverConfig.setBeaconOff() 
Turn on the beacon: TranceiverConfig.TranceiverConfig.setBeaconOn() 
Set the Transceiver to low power mode:  TranceiverConfig.TranceiverConfig.setLowPowerMode()
Read in the internal temperature of the transceiver: TranceiverConfig.TranceiverConfig.read()  







UV Driver:
--
Location: ../Drivers/UV/UVDriver.py

Functionality:
	The UV Driver inherits functionality from the ADC Driver, much like the Sun Sensor Driver. It reads from a specific channel through the SPi connection created in the ADC Driver, and returns a single value. To get the data returned by this driver call UVDriver.UVDriver.read()
	

