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
int main(void)
{
    int bytes;

    //open the serial ports
    int txPort = open(UART_PORT, O_RDWR | O_NOCTTY ); 
    if (txPort == -1)
    {
        printf ("Error no is : %d\n", errno);
        printf("Error opening serial port\n");
        exit(1);
    }
    
    //check the num of bytes in the buff
    ioctl(txPort, FIONREAD, &bytes);

    //tell python where or not there is stuff in the buff
    if(bytes > 0)
    {
        PRINT_DEBUG(bytes)
        exit(1);
    }
    else
    {
        PRINT_DEBUG(bytes)
        exit(0);
    }
    
}