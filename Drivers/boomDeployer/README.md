Boom Deployer Driver:
--
Location: ../Drivers/boomDeployer/BoomDeployer.py

Functionality:
	Our AeroBoom is stored in a container held shut by wire. The Boom Deployer Driver will set up a connection to various pins. These pins will be connected to both the wire cutters. After this connection is made the Driver will tell the first wire cutter to turn on for three seconds and then turn off. It will do this twice. Since there is no way for us to tell if the first wire cutter was successful we will then turn on the second wire cutter and run it in the same manner. This ensures that the AeroBoom gets deployed. The AeroBoom gets deployed by calling: boomDeployer.BoomDeployer.deploy()
