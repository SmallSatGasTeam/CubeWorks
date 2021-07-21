#include <stdio.h>
#include <stdlib.h>

char cammand0 [] = "cd CubeWorks0/ ; git fetch ; git stash ; git pull";
char cammand1 [] = "cd CubeWorks1/ ; git fetch ; git stash ; git pull";
char cammand2 [] = "cd CubeWorks2/ ; git fetch ; git stash ; git pull";
char cammand3 [] = "cd CubeWorks3/ ; git fetch ; git stash ; git pull";
char cammand4 [] = "cd CubeWorks4/ ; git fetch ; git stash ; git pull";
char upDateStartUpCode [] = "cd CubeWorks0/ ; gcc startup.c -o startup.exe ; ";
char upDateStartUpCode2 [] = "cd CubeWorks0/ ; cp startup.exe ~/ ; rm startup.exe";

char branchCommand0 [] = "cd ; cd CubeWorks0/TXISR/TXServiceCode ; gcc TXServiceCode.c -o TXService.run";
char branchCommand1 [] = "cd ; cd CubeWorks1/TXISR/TXServiceCode ; gcc TXServiceCode.c -o TXService.run";
char branchCommand2 [] = "cd ; cd CubeWorks2/TXISR/TXServiceCode ; gcc TXServiceCode.c -o TXService.run";
char branchCommand3 [] = "cd ; cd CubeWorks3/TXISR/TXServiceCode ; gcc TXServiceCode.c -o TXService.run";
char branchCommand4 [] = "cd ; cd CubeWorks4/TXISR/TXServiceCode ; gcc TXServiceCode.c -o TXService.run";

char branchCommand5 [] = "cd ; cd CubeWorks0/TXISR/TXServiceCode ; rm TXService.run";
char branchCommand6 [] = "cd ; cd CubeWorks1/TXISR/TXServiceCode ; rm TXService.run";
char branchCommand7 [] = "cd ; cd CubeWorks2/TXISR/TXServiceCode ; rm TXService.run";
char branchCommand8 [] = "cd ; cd CubeWorks3/TXISR/TXServiceCode ; rm TXService.run";
char branchCommand9 [] = "cd ; cd CubeWorks4/TXISR/TXServiceCode ; rm TXService.run";
//compile testing code
char testingCommand [] = "cd ; cd CubeWorks0/ ; gcc setNewTXWindow.c -o setNewTXWindow.exe ; sudo cp setNewTXWindow.exe ~/TXISRData ; rm setNewTXWindow.exe";

char configCommand1 [] = "cd ; cd CubeWorks0/ ; gcc flightConfig.c -o flightConfig.exe ; cp flightConfig.exe ~/ ; rm flightConfig.exe";
char configCommand2 [] = "cd ; cd CubeWorks0/ ; gcc flightConfigWifi.c -o flightConfigWifi.exe ; cp flightConfigWifi.exe ~/ ; rm flightConfigWifi.exe";

void main()
{
    system(cammand0);
    system(cammand1);
    system(cammand2);
    system(cammand3);
    system(cammand4);
    system(upDateStartUpCode);
    system(upDateStartUpCode2);

    printf("\n>>>Creating tx routine for CubeWorks0<<<\n");
    system(branchCommand5);
    system(branchCommand0);
    printf("\n>>>Creating tx routine for CubeWorks1<<<\n");
    system(branchCommand6);
    system(branchCommand1);
    printf("\n>>>Creating tx routine for CubeWorks2<<<\n");
    system(branchCommand7);
    system(branchCommand2);
    printf("\n>>>Creating tx routine for CubeWorks3<<<\n");
    system(branchCommand8);
    system(branchCommand3);
    printf("\n>>>Creating tx routine for CubeWorks4<<<\n");
    system(branchCommand9);
    system(branchCommand4);
    printf("\n>>>Compiling testing code<<<\n");
    system(testingCommand);

    printf("\n>>>Building configuration code<<<\n");
    system(configCommand1);
    system(configCommand2);

    printf(">>>Everything is up to date\n");
}

//this code will update all the code bases 
//Written by Shawn