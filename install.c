#include <stdio.h>
#include <stdlib.h>


//this will handle the install of all gas software
char GIT_CODE_BASE [] ="https://github.com/SmallSatGasTeam/CubeWorks.git";
char crontabComand [] ="@reboot sudo runuser pi -c ./startup.exe";

char cammand0 [] = "git clone -b codeBase https://github.com/SmallSatGasTeam/CubeWorks.git CubeWorks0/";
char cammand1 [] = "git clone -b codeBase https://github.com/SmallSatGasTeam/CubeWorks.git CubeWorks1/";
char cammand2 [] = "git clone -b codeBase https://github.com/SmallSatGasTeam/CubeWorks.git CubeWorks2/";
char cammand3 [] = "git clone -b codeBase https://github.com/SmallSatGasTeam/CubeWorks.git CubeWorks3/";
char cammand4 [] = "git clone -b codeBase https://github.com/SmallSatGasTeam/CubeWorks.git CubeWorks4/";

// char brnachCommand0 [] = "cd ; cd CubeWorks0; git checkout codebase; cd ;";
// char brnachCommand1 [] = "cd ; cd CubeWorks1; git checkout codebase; cd ;";
// char brnachCommand2 [] = "cd ; cd CubeWorks2; git checkout codebase; cd ;";
// char brnachCommand3 [] = "cd ; cd CubeWorks3; git checkout codebase; cd ;";
// char brnachCommand4 [] = "cd ; cd CubeWorks4; git checkout codebase; cd ;";

// #update and install python
// #NO long in use cause the version are lock for FLIGHT!
// # sudo apt full-upgrade
// # sudo apt-get update
// # sudo apt install python3
// # sudo apt install python3-pip
// # sudo apt install python3-numpy
// # sudo apt install git 

void main()
{
    char buff[100] ;
    printf("\n>>>Creating a CubeWorks0<<<\n");
    //install the first code base
    system(cammand0);

    // //install the code bases
    printf("\n>>>Creating a CubeWorks1<<<\n");
    system(cammand1);

    printf("\n>>>Creating a CubeWorks2<<<\n");
    system(cammand2);

    printf("\n>>>Creating a CubeWorks3<<<\n");
    system(cammand3);

    printf("\n>>>Creating a CubeWorks4<<<\n");
    system(cammand4);
    
    #ifdef NOT_MAIN
        //these lines are for testing on other branches!
        system(brnachCommand0);
        system(brnachCommand1);
        system(brnachCommand2);
        system(brnachCommand3);
        system(brnachCommand4);
    #endif

    //up date the crontab to run the startup.exe
    printf("\n>>>creating start up proticol<<<\n");
    system("sudo crontab -l > mycron");  
    system("echo $crontabComand >> mycron");
    system("sudo crontab mycron");
    system("rm mycron");

    //create the start up code, and then move it to the root
    printf("\n>>>creating multi-code base proticol\n");
    system("cd CubeWorks0\ngcc startup.c -o startup.exe\ncp startup.exe ~/");

    printf(">>rebooting to finish installation<<<"); 
    system("sudo reboot");
}