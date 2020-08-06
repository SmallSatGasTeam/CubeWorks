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
    ioctl(UART_PORT, FIONREAD, &bytes);
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