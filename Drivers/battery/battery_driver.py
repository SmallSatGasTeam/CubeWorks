from Drivers.Driver import Driver
from math import trunc
import smbus

class Battery(Driver):
    def __init__(self):
        """
        Calls back to the parent (Driver)  constructor, sets up the i2c interface for the battery. TODO: After have EPS, write fault tolerance. Taken from: https://learn.sparkfun.com/tutorials/python-programming-tutorial-getting-started-with-the-raspberry-pi/experiment-4-i2c-temperature-sensor
        """
        super().__init__("Battery")

        # i2c channel
        self.itc_ch = 1

        # This value is the address of the battery on the i2c bus, this may not end bup being 0x48
        self.i2c_address = 0x48

        # Register address
        self.reg_battery = 0x48
        self.reg_config = 0x01

        # init i2c (SMBus)
        self.bus = smbus.SMBus(i2c_ch)

        # read the CONFIG register (2 bytes)
        val = this.bus.read_i2c_block_data(this.i2c_address, this.reg_config, 2)

        # set to 4 hz sampling (CR1, CR0 = 0b10)
        val[1] = val[1] & 0b00111111
        val[1] = val[1] | (0b10 << 6)

        # Write 4 hz sampling back to CONFIG
        this.bus.write_i2c_block_data(this.i2c_address, this.i2c_config, 2)

    def read(self):
        """Returns the value of the most recent voltage taken."""
        return latest_voltage = self.bus.read_i2c_block_data(i2c_address, this.reg_battery, 2)
        



