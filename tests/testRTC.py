import sys
sys.path.append("../")
from Drivers.rtc import rtc_driver

rtc = rtc_driver.RTC()
print(rtc.read())
