#!/bin/bash

# This file will do the following to reset the flight logic to its initial state:
# - Erase all pictures
# - Erase flight logic boot records and replace with 3 lines of 0s. Note, both bootRecords and backupBootRecords need to be reset.
# - Erase recorded Attitude, TTNC, Deploy data
# - Erase TXISR windows and txFile
# - Erase TXISR flags file and set it to 5 rows of 0s
# - Erase transmissionFlag file and set to Enabled
# - Erase AX25Flag file and set to Disabled

# Erase pictures
rm -rf ../../flightLogicData/Pictures/*

# Erase flight logic boot records and replace with 3 lines of 0s. Note, bootRecords and backupBootRecords need to be erased.
cat /dev/null > ../flightLogic/bootRecords
cat /dev/null > ../flightLogic/backupBootRecords
echo -n -e "0\n0\n0\n" > ../flightLogic/bootRecords
echo -n -e "0\n0\n0\n" > ../flightLogic/backupBootRecords

# Erase Attitude, TTNC, Deploy data
cat /dev/null > ../flightLogic/data/Attitude_Data.txt
cat /dev/null > ../flightLogic/data/TTNC_Data.txt
cat /dev/null > ../flightLogic/data/Deploy_Data.txt

# Erase TXISR windows and txFile
cat /dev/null > ../TXISR/data/txWindows.txt
cat /dev/null > ../TXISR/data/txFile.txt

# Erase TXISR flags file and set it to 5 rows of 0s
cat /dev/null > ../TXISR/data/flagsFile.txt
echo -n -e "0\n0\n0\n0\n0\n" > ../TXISR/data/flagsFile.txt

# Set Enable transmission flag
cat /dev/null > ../TXISR/data/transmissionFlag.txt
echo -n -e "Enabled" > ../TXISR/data/transmissionFlag.txt

# Set Disable AX25 flag
cat /dev/null > ../TXISR/data/AX25Flag.txt
echo -n -e "Disabled" > ../TXISR/data/AX25Flag.txt

# Print All Done
echo "Flight logic successfully reset"
