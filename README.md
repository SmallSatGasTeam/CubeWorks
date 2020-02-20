# GASPACS
Flight software for the GASPACS mission 

## Introduciton
The Get Away Special Passive Attitude Control Satellite (GASPACS) is an experimental 1U cubesat in development by Utah State University's Get Away Special team.  The purpose of the experiment is to test the viability of an inflatable aero-stablization boom deployable component in Low Earth Orbit (LEO).  This repository contains the flight software for the satellite.

## Installation
The GASPACS software module is designed to run on a Raspberry Pi Zero W running Raspbian as its operating system.  For production, Raspbian without the desktop environment will be used, but during development the DE is fine to use.

### Installation Process
1. Obtain a copy of Raspbian from RaspberryPi.org.
2. Obtain a copy of Balena Etcher (for flashing the OS onto the SD card).
3. Using Etcher, flash Raspbian to the SD Card.
4. Insert the SD card into the Raspberry Pi Zero W, and apply power to the Pi.
5. Once booted, install the following dependencies:
	- Python3
	- TODO: compile list of dependencies
6. Copy this repository onto the Pi (preferably in the home directory, but it shouldn't matter).
	- It doesn't matter how it gets there, using git, scp, a flash drive, telepathy, etc. just get the files on there.
7. Once everything is there, run the main python file with the following command:
```
$ python3 main.py
```

## Git Tutorial
For those on the team who would like a bit of extra help with git, here are the basics of interacting with git and GitHub over the command line.

### Pulling from GitHub
It's a good idea to do this every time you sit down to work on the code in the repository, as it helps avoid merge conflicts.  
1. From the root directory of the git repository: `git pull origin master`

### How to push to GitHub
Do this frequently, at least always when you are done with every programming session. 
1. From the root directory of the git repository: `git add .`
2. Type: `git commit -m "<your comment here>"`
3. Type: `git push origin master`
