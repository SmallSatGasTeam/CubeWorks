import time
import sys
from spidev import SpiDev

dev = SpiDev(0,0)
dev.max_speed_hz = 10

try:
    while True:
        dev.writebytes([1,2,4,8,16,32,64,128])
        time.sleep(0.001)
except KeyboardInterrupt:
    sys.exit(0)
