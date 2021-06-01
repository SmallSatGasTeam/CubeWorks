#include <termios.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

#define MESSAGE "474153504143530000000019003c0000000000000039b2cfafd06ed43f29d5478b719fa73247415350414353"

struct termios options;
void setUpUart();

int main(void){
    int txPort = open("/dev/serial0", 02 | 0400);
    if(txPort == -1){
        printf("Error, couldn't open the serial port.\n");
        exit(1);
    }
    setUpUart();

    for(;;){
        write(txPort, "ES+W22003321\r", 13);
        sleep(1);
        write(txPort, "ES+W22003321\r", 13);
        sleep(1);
        printf("Sending Data.\n");
        write(txPort, MESSAGE, 89);
    }

    return 0;
}

void setUpUart(){
    cfsetspeed(&options, B115200);

    //set up the number of data bits
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8;
}