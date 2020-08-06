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
    //NOTE: opening the serial port clears the buffer!!!
    int txPort = open(UART_PORT, O_RDWR | O_NOCTTY ); 
    if (txPort == -1)
    {
        printf ("Error no is : %d\n", errno);
        printf("Error opening serial port\n");
        exit(1);
    }

    
    while(1)
    {
        //check the num of bytes in the buff
        ioctl(txPort, FIONREAD, &bytes);
        //exit if we see a byte
        if(bytes > 0) exit(1);
        //print value 
        PRINT_DEBUG(bytes)
    }
    
    
}