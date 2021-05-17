# CubeWorks
Flight software for the GASPACS mission written in Python, with some compents in c.

## Introduction
The Get Away Special Passive Attitude Control Satellite (GASPACS) is an experimental 1U cubesat in development by Utah State University's Get Away Special team.  The purpose of the experiment is to test the viability of an inflatable aero-stabilization boom deployable component in Low Earth Orbit (LEO).  This repository contains CubeWorks, the flight software for the satellite.

## Objectives
CubeWorks is intended to be a robust, modular, and fault tolerant software framework for small satellites, with minimal barrier to entry.  The experienced developer may be asking, "Why write the entire framework in python and not a more performant language with closer hardware interaction?"  The answer is because the framework is designed to be accessible to newer developers who want to get into space research.  The software isn't as performant as an equivalent solution written in, say, c++ but it isn't designed to be.   

Framework components are designed to be modular, and easy to add to and remove from a given system.  All that is needed is to define a driver that interacts with your hardware components and inherits from the built in `Component` class, and include it in the main file.  

## Installation
The CubeWorks software module is designed to run on a Raspberry Pi Zero W running Raspbian lite os as its operating system.  For production, Raspbian without the desktop environment will be used, but during development the DE is fine to use.  For development, using a Raspberry Pi 3 B+ is fine.  The framework has not been tested on a Pi 4, but since it's all in python, it should run just fine.  

### Installation Process
1. Image a Raspberry Pi with Raspbian lite and boot the Pi
2. Use `sudo raspi-config` to set the proper network settings, set a user password, localisation options.
3. Under Interfacing Options enable Camera, SSH, SPI, I2C, and Serial ("No" to login shell, "Yes" to serial interface)
3. Update all packages with the commands: `sudo apt update` `sudo apt full-upgrade`
4. Reboot, install the following dependencies:
	- Python3, `sudo apt install python3`
	- python3-pip, `sudo apt install python3-pip`
	- NumPy, `sudo apt install python3-numpy`
5. Create the exe file to run for the installation process, run "gcc install.c -o install.exe"
6. run "./install.exe"

### RUN ON STARTUP
To run the testMainFlightLogic.py file (or any other program) on startup, run `sudo crontab -e` and then add the following line to the end of the file:
`@reboot sudo runuser pi -c "cd ; ./startup.exe"`. NOTE: this command is already part of the image. 

## Documentation

This project is documented using Doxygen.  Instructions for building the docs are located in `CubeWorks/docs/README.md`.  

### File Structure
This file structure comprises the major compoments of CubeWorks.  

```
CubeWorks
├── Components
│   ├── Component.py
│   ├── ContextPrinter.py
│   ├── Database.py
│   └── __init__.py
├── Drivers
│   ├── driver0
│   │   ├── driver0.py
│   │   └── __init__.py
│   └── driver1
│       ├── driver1.py
│       └── __init__.py
├── main.py
├── mission_modes.py
├── README.md
├── tests
│   └── unit_testing_example.py
├── unit_tests.py
└── watchdog
```

### Class Structure

![class](https://user-images.githubusercontent.com/27446370/118514932-23915500-b6f2-11eb-9dde-4a1bd2eee4df.png)


###Data Flows:

[GAS software.pdf](https://github.com/SmallSatGasTeam/CubeWorks/files/6494865/GAS.software.pdf)

[Boom deploy data flow.pdf](https://github.com/SmallSatGasTeam/CubeWorks/files/6494888/Boom.deploy.data.flow.pdf)

[Data recived data flow.pdf](https://github.com/SmallSatGasTeam/CubeWorks/files/6494890/Data.recived.data.flow.pdf)

[Decode TX data flow.pdf](https://github.com/SmallSatGasTeam/CubeWorks/files/6494891/Decode.TX.data.flow.pdf)

[multi save data path.pdf](https://github.com/SmallSatGasTeam/CubeWorks/files/6494892/multi.save.data.path.pdf)

[multi save data path2.pdf](https://github.com/SmallSatGasTeam/CubeWorks/files/6494893/multi.save.data.path2.pdf)

[Post Boom deploy data flow.pdf](https://github.com/SmallSatGasTeam/CubeWorks/files/6494894/Post.Boom.deploy.data.flow.pdf)

[preboom deploy data flow.pdf](https://github.com/SmallSatGasTeam/CubeWorks/files/6494895/preboom.deploy.data.flow.pdf)

[prepare for tx data flow.pdf](https://github.com/SmallSatGasTeam/CubeWorks/files/6494896/prepare.for.tx.data.flow.pdf)
