Transceiver Configuration Driver:
--
Location: ../Drivers/tranceiverConfig/TranceiverConfig.py

Functionality:
	The Transceiver Configuration Driver does not handle the transmissions. It does, however, turn on and off the beacon, turn on low power mode, and read the internal temperature sensor. To access these different capabilities see the following commands:
Turn off the beacon: TranceiverConfig.TranceiverConfig.setBeaconOff() 
Turn on the beacon: TranceiverConfig.TranceiverConfig.setBeaconOn() 
Set the Transceiver to low power mode:  TranceiverConfig.TranceiverConfig.setLowPowerMode()
Read in the internal temperature of the transceiver: TranceiverConfig.TranceiverConfig.read()  
