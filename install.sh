#!/bin/bash
# rsync using variables
#this will handle the install of all gas software
gitCodeBase = https://github.com/SmallSatGasTeam/CubeWorks.git
crontabComand = @reboot sudo runuser pi -c ./startup.exe

#update and install python
sudo apt full-upgrade
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-numpy
sudo apt install git 

#install the first code base
mkdir CubeWorks0
cd ~/CubeWorks0 ; git clone $gitCodeBase

#install all the required packages
cd ; cd ~/CubeWorks0/CubeWorks ; $ echo \n\n\n>>>starting requirements install<<<\n\n\n; pip3 install -r requirements.txt ; cd ;

#create the start up code, and then move it to the root
cd ; cd ~/CubeWorks0/CubeWorks ; $ echo creating multi-code base proticol ; gcc startup.c -o startup.exe ; cp startup.exe ~/

#up date the crontab to run the startup.exe
crontab -e $crontabComand

#install the code bases
cd ; mkdir CubeWorks1
cd ~/CubeWorks1 ; git clone $gitCodeBase
cd ; mkdir CubeWorks2
cd ~/CubeWorks2 ; git clone $gitCodeBase
cd ; mkdir CubeWorks3
cd ~/CubeWorks3 ; git clone $gitCodeBase
cd ; mkdir CubeWorks4
cd ~/CubeWorks4 ; git clone $gitCodeBase

$ echo \n\n\n>>>rebooting to finish installation<<<\n\n\n 
sudo reboot 