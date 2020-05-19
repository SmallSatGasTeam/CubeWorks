import smbus

class ESP:
    def __init__(self):
        self.__DEVICE_BUS = 1
        self.__DEVICE_ADDR = 0x18
        self.__RegisterADR = 0x00
        self.__bus = smbus.SMBus(DEVICE_BUS)
    
    def getCurrent():
        super().__init__("ESP")
        bus.write_byte_data(self.__DEVICE_ADDR, self.__RegisterADR, 0x01)

    def __startRead(command)
        bus.write_byte_data(self.__DEVICE_ADDR, self.__RegisterADR, 0x01)