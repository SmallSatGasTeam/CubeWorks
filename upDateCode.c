#include <stdio.h>
#include <stdlib.h>

char cammand0 [] = "cd CubeWorks0/ ; git fetch ; git pull";
char cammand1 [] = "cd CubeWorks1/ ; git fetch ; git pull";
char cammand2 [] = "cd CubeWorks2/ ; git fetch ; git pull";
char cammand3 [] = "cd CubeWorks3/ ; git fetch ; git pull";
char cammand4 [] = "cd CubeWorks4/ ; git fetch ; git pull";
char upDateStartUpCode [] = "cd CubeWorks0/ ; gcc startup.c -o startup.exe ; cp startup.exe ~/ ; rm startup.exe";


void main()
{
    system(cammand0);
    system(cammand1);
    system(cammand2);
    system(cammand3);
    system(cammand4);
    system(upDateStartUpCode);


    printf(">>>Everything is up to date\n");
}

//this code will update all the code bases 
//Written by Shawn