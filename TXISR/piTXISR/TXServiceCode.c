//#include <unistd.d>
#include <fcntl.h>
#include <termios.h>
#include <stdio.h>
#include <stdlib.h>
//Take just the DEBUG line out when your are done debugging and leave debug.h
#define DEBUG
#include "debug.h"

#define ENABLE "conifPinTXISR"
#define DISABLE "conifPinTXISRDone"
#define FLAG_FILE "./out.txt" //change this later for the real program
#define FORMAT_FILE "./temp.txt" //this is the file that dallan will creat


void main(int argc,char* argv[])
{
    int numOfRecords = argv[1];
    int dataType = argv[2];

    FILE *txFile;
    if (!(txFile = fopen(FORMAT_FILE,"r")))
    {
        //if we fail exit
        DEBUG_P(Failed to open file)
        exit(1);
    }

    //config linuxs to give us the pins
    int enable = system(ENABLE);
    //if we fail reboot
    if(enable == -1) 
    {
        DEBUG_P(Failed to connect to tx pin)
        exit(1);
    } 

    //

    //read in all the lines of a file
    char ch = fgetc(txFile);
    //set up array for tx, the max is 128, so we better not exceed that anyways so using an array of 128 is fine.
    char line[128] = {0};
    DEBUG_P(Printing file>>>);
    while(ch != EOF)
    {
        PRINT_DEBUG_CHAR('\n')
        //get the size of each line in the file
        int charCount = 0;
        for (int i = 0; i < 128; i++)
        {
            line[i] = "0";
        }
        while(ch != 10 && ch != EOF)
        {
            //save all the data in that line
            line[charCount++] = ch;
            ch = fgetc(txFile);
        }
        //transmit the data
        #ifdef DEBUG
            for(int i = 0; i < charCount; i++)
            {
                PRINT_DEBUG_CHAR(line[i]) 
            }
            PRINT_DEBUG_CHAR('\n')
        #endif
        if(ch == 10 && ch != EOF)
        {
            ch = fgetc(txFile);
        }
    } 

    



    //debuging
    // int ret = system("echo hello world");
    // if(ret == 0) printf("It worked\n");
    // else if (ret == -1) printf("didn't work\n");
    // printf("The value of ret: %d\n", ret);
}