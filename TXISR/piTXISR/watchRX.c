#include <unistd.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <time.h>
#include <fcntl.h>
#include <termios.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <stdint.h>
//Take just the DEBUG line out when your are done debugging and leave debug.h
#define DEBUG
#include "debug.h"
#define UART_PORT "/dev/ttyAMA0" //this is serial port name, make sure this is correct for the final code

#include <sys/ioctl.h>

//this sets control of the settings for our serial port
struct termios options;

void setUpUart();

int main(void)
{
    long unsigned bytes = 0;

    //open the serial ports
    //NOTE: opening the serial port clears
    int txPort = open(UART_PORT, O_RDWR | O_NOCTTY ); 
    if (txPort == -1)
    {
        printf ("Error no is : %d\n", errno);
        printf("Error opening serial port\n");
        exit(1);
    }
    setUpUart();

    //check the num of bytes in the buff
    while(bytes == 0)
    {
        ioctl(txPort, FIONREAD, &bytes);
    }

    //tell python where or not there is stuff in the buff
    if(bytes > 0)
    {
        //print the num of bytes to the screen
        printf("%lu\n", &bytes);
        exit(1);
    }
    else
    {
        printf("0\n");
        exit(0);
    }
    
}


/*******************************************************************************************
 * setUpUart
 * this func sets up the uart commincation for us so everything works nicely
 *******************************************************************************************/
void setUpUart()
{
    //set the baud rate, it is the number with a b infornt of it ex 115200 -> B115200
    //BOUD_RATE
    cfsetspeed(&options, B115200);

    //set up the number of data bits
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8;
}