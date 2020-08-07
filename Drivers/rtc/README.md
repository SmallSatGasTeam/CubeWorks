RTC Driver:
--
Location: ../Drivers/rtc/rtc_driver.py

Functionality:
	The RTC Driver is perhaps the most simple driver. All it does is read the system clock and return the value found there.This value will be the time in milliseconds since the Unix Epoch To get that value call: rtc_driver.RTC.read().
