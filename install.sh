#!/bin/bash
#this will handle the install of all gas software
sudo apt full-upgrade
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-numpy
cd ; cd ~/CubeWorks ; pip3 install -r requirements.txt ; cd ;