#include <unistd.d>
#include <fcntl.h>
#include <termios.h>
#include <stdio.h>
#include <stdlib.h>

#define ENABLE "conifPinTXISR"
#define DISABLE "conifPinTXISRDone"
#define FLAG_FILE "./out.txt" //change this later for the real program


void main(int argc,char* argv[])
{
    int numOfRecords = argv[2];
    int dataType = argv[3];

    //open the transmition file
    FILE *txFile;
    if ((txFile = fopen(argv[1],"r")))
    {
        //if we fail reboot
        fclose(txFile);
        exit(1);
    }

    //config linuxs to give us the pins
    int enable = system(ENABLE);
    //if we fail reboot
    if(enable == -1) exit(1); 



    //debuging
    // int ret = system("echo hello world");
    // if(ret == 0) printf("It worked\n");
    // else if (ret == -1) printf("didn't work\n");
    // printf("The value of ret: %d\n", ret);
}