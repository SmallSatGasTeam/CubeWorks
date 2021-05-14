#!/usr/bin/env bash
# rsync using variables
#this will handle the install of all gas software
GIT_CODE_BASE="https://github.com/SmallSatGasTeam/CubeWorks.git"
crontabComand="@reboot sudo runuser pi -c /home/pi/./startup.exe"
#this is the branch we are using , if you want maste leave it blank exe " "
branch="codeBase";
#update and install python
#NO long in use cause the version are lock for FLIGHT!
# sudo apt full-upgrade
# sudo apt-get update
# sudo apt install python3
# sudo apt install python3-pip
# sudo apt install python3-numpy
# sudo apt install git 


printf "\n>>>Creating a CubeWorks0<<<\n";
#install the first code base
git clone $GIT_CODE_BASE CubeWorks0;

printf "\n>>>Creating a CubeWorks1<<<\n";
#install the code bases
git clone $GIT_CODE_BASE CubeWorks1;
#TESTING LINE
cd CubeWorks1/ ; git checkout $branch ;

#this line is testing only!
cd ; cd CubeWorks0/ ; git checkout $branch; cd ;

printf "\n>>>Creating a CubeWorks2<<<\n";
#this line is for testing 
git clone $GIT_CODE_BASE CubeWorks2;
#TESTING LINE
cd CubeWorks2/ ; git checkout $branch ;

printf "\n>>>Creating a CubeWorks3<<<\n";
#git clone $GIT_CODE_BASE CubeWorks3;
git clone $GIT_CODE_BASE CubeWorks3;
#TESTING LINE
cd CubeWorks3/ ; git checkout $branch ;

printf "\n>>>Creating a CubeWorks4<<<\n";
#git clone $GIT_CODE_BASE CubeWorks4;
git clone $GIT_CODE_BASE CubeWorks4;
#TESTING LINE
cd CubeWorks4/ ; git checkout $branch ;

#create the start up code, and then move it to the root
cd ; cd CubeWorks0/ ; printf "\n>>>creating multi-code base proticol\n"; gcc startup.c -o startup.exe ; cp startup.exe ~/


#up date the crontab to run the startup.exe
#crontab -e $crontabComand
printf "\n>>>creating start up proticol<<<\n"
sudo crontab -l > mycron  
echo $crontabComand >> mycron
sudo crontab mycron
rm mycron

echo ">>rebooting to finish installation<<<" 
#sudo reboot