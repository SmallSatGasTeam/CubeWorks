# Set baud rate
stty -F /dev/ttyUSB0 115200
# Put local radio into pipe mode
echo 'ES+W23003421' > /dev/ttyUSB0
sleep .1
# put remote radio into pipe mode
echo 'ES+W22003461' > /dev/ttyUSB0
sleep .1
# send message

sleep .1
head -c 100 ~/Pictures/SSDV-Test/output1.bin > /dev/ttyUSB0
