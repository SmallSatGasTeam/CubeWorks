Backup Antenna Deployment Driver:
--
Location:  ../Drivers/backupAntennaDeployerBackupAntennaDeployer.py

Functionality: 
	The Backup Antenna Deployment Driver sets up a connection to various pins. These pins are connected to capacitors that power the Antenna Doors. Through this connection the software will set the capacitors to turn on and open the Antenna Doors. This code will be used as a fail safe if the premade software to open the Antenna Doors is unsuccessful. The Antenna can be manually deployed by calling: BackupAntennaDeployer.BackupAntennaDeployer.deploy().
