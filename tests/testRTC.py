import sys
<<<<<<< HEAD
sys.path.append('../')
from Drivers.rtc import RTC
rtc = RTC()
=======
sys.path.append("../")
from Drivers.rtc import rtc_driver

rtc = rtc_driver.RTC()
>>>>>>> 1938fa3dcf35eeafbbc393d6416c04bcbeb561e3
print(rtc.read())
