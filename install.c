#include <stdio.h>
#include <stdlib.h>


//this will handle the install of all gas software
char GIT_CODE_BASE [] ="https://github.com/SmallSatGasTeam/CubeWorks.git";
char crontabComand [] ="@reboot sudo runuser pi -c ./startup.exe";


//to change the branch take out the -b codeBase for master or change it to a different branch.
char cammand0 [] = "git clone -b codeBase https://github.com/SmallSatGasTeam/CubeWorks.git CubeWorks0/";
char cammand1 [] = "git clone -b codeBase https://github.com/SmallSatGasTeam/CubeWorks.git CubeWorks1/";
char cammand2 [] = "git clone -b codeBase https://github.com/SmallSatGasTeam/CubeWorks.git CubeWorks2/";
char cammand3 [] = "git clone -b codeBase https://github.com/SmallSatGasTeam/CubeWorks.git CubeWorks3/";
char cammand4 [] = "git clone -b codeBase https://github.com/SmallSatGasTeam/CubeWorks.git CubeWorks4/";

//this code compiles the c code that is need to run transmission. 
char branchCommand0 [] = "cd ; cd CubeWorks0/TXISR/TXServiceCode ; gcc TXServiceCode.c -o TXService.run; cd ;";
char branchCommand1 [] = "cd ; cd CubeWorks1/TXISR/TXServiceCode ; gcc TXServiceCode.c -o TXService.run; cd ;";
char branchCommand2 [] = "cd ; cd CubeWorks1/TXISR/TXServiceCode ; gcc TXServiceCode.c -o TXService.run; cd ;";
char branchCommand3 [] = "cd ; cd CubeWorks1/TXISR/TXServiceCode ; gcc TXServiceCode.c -o TXService.run; cd ;";
char branchCommand4 [] = "cd ; cd CubeWorks1/TXISR/TXServiceCode ; gcc TXServiceCode.c -o TXService.run; cd ;";

char upDateCommand [] = "cd ; cd CubeWorks0/ ; gcc upDateCode.c -o upDateCode.exe ; cp upDateCode.exe ~/ ; rm upDateCode.exe";

char testingCommand [] = "cd ; cd CubeWorks0/ ; gcc setNewTXWindow.c -o setNewTXWindow.exe ; sudo cp setNewTXWindow.exe ~/TXISRData ; rm setNewTXWindow.exe";




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
    

    //complie the code
    printf("\n>>>Creating tx routine for CubeWorks0<<<\n");
    system(branchCommand0);
    printf("\n>>>Creating tx routine for CubeWorks1<<<\n");
    system(branchCommand1);
    printf("\n>>>Creating tx routine for CubeWorks2<<<\n");
    system(branchCommand2);
    printf("\n>>>Creating tx routine for CubeWorks3<<<\n");
    system(branchCommand3);
    printf("\n>>>Creating tx routine for CubeWorks4<<<\n");
    system(branchCommand4);

    //create the upDate code 
    printf("\n>>>Creating update code<<<\n");
    system(upDateCommand);

    //Create the set new txWindows code
    printf("\n>>>Creating setTXWindows routine<<<\n");
    system(testingCommand);

    //create the start up code, and then move it to the root
    printf("\n>>>creating multi-code base protocol\n");
    system("cd CubeWorks0\ngcc startup.c -o startup.exe\ncp startup.exe ~/");
    

    //up date the crontab to run the startup.exe
    // printf("\n>>>creating start up proticol<<<\n");
    // system("sudo crontab -l > mycron");  
    // system("echo @reboot sudo runuser pi -c cd ; ./startup.exe >> mycron");
    // system("sudo crontab mycron");
    // system("rm mycron");


    printf(">>rebooting to finish installation<<<\n"); 
    system("sudo reboot");
}