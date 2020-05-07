#!/bin/bash
# Set baud rate
stty -F /dev/ttyUSB0 115200
# Clean Picture Directory
rm ~/Pictures/SSDV-Test/Transmission/*
# Take Picture
raspistill -o ~/Pictures/SSDV-Test/Transmission/picture.jpeg -w 640 -h 480
# Convert Picture with SSDV
ssdv -e ~/Pictures/SSDV-Test/Transmission/picture.jpeg ~/Pictures/SSDV-Test/Transmission/picture.bin
# Convert Picture from Hex to Ascii
xxd ~/Pictures/SSDV-Test/Transmission/picture.bin > ~/Pictures/SSDV-Test/Transmission/picture.txt
# Split text file into 126 byte chunks
split -b 126 -a 0 -d ~/Pictures/SSDV-Test/Transmission/picture.txt ~/Pictures/SSDV-Test/Transmission/Packets/
# Put local radio into pipe mode
sleep .15
echo 'ES+W23003421' > /dev/ttyUSB0
sleep .15
# put remote radio into pipe mode
echo 'ES+W22003461' > /dev/ttyUSB0
sleep .15
# send message
set -- x*
files=~/Pictures/SSDV-Test/Transmission/Packets/*
for i in $files;
do
  echo $i
  cat $i > /dev/ttyUSB0
  sleep .15
done
