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

#define UART_PORT "/dev/serial0" //this is serial port name, make sure this is correct for the final code

//this is our time delay
#define DELAY_tx 120

//this defines are for the data types
#define MAX_BYTES_PER_LINE 256
#define MAX_NUM_OF_DATA_TYPES 5
#define DELAY_UNTIL_TX_WINDOW 5000
#define SIZE_OF_TIME_STAMP 10
#define PHOTO_TYPE 3
#define TIME_DEVISOR ':'
#define COMMAND_SIZE 30

//NOTE: becasue of how we have to set the boud rate I cannot use a define for it in ceritian places, just do a contrl f and look for BOUD_RATE
//it is place next to every place that the boud rate is used, you also need to change the define as it is used as well.
//NOTE: this boud rate (9600) is the radio speed. We talk to it with a diffrent speed, in other words the 9600 is our divisor for the delay
#define BOUD_RATE 9600


//this sets control of the settings for our serial port
struct termios options;

void setUpUart();
void getInput(char * a);

//returns ms since the epoch
intmax_t millis()
{
    struct timespec current_time;
    clock_gettime(CLOCK_MONOTONIC_RAW, &current_time);
    //get the milli seconds
    intmax_t a = ((current_time.tv_sec) * 1000) + ((current_time.tv_nsec) / 1000000);
    return a;
}



/*******************************************************************************************
 * sudo code: Main
 * this first tries to open the file it is trying to send
 * then it tries to take control of the serial ports
 * then it tries to open the serial port
 * then it reads each line of the file and sends it one at a time
 *      NOTE: the program will wait x number of millaseconds inbetween each line it sends
 *            depending on what the radio needs
 * After it has sent everything it opens the flags file and records the time of the last
 *      sent record
 * It then closes the serial port
 * it then returns control back to linuxs
 * Program then exits
 *******************************************************************************************/
int main(int argc,char* argv[])
{
    DEBUG_P(Began main)
    intmax_t startTime = millis();
    intmax_t currentTime = millis();
    intmax_t startTimeTX = 0;
    intmax_t currentTimeTX = 0;
    char data[COMMAND_SIZE];
    DEBUG_P(Made it past all of these variable instantiations)
    //gather user input
    getInput(&data);
    //DEBUG_P(Made it past the problem spot)
    int transmissionWindow = 0;


    //open the serial ports
    //NOTE: opening the serial port clears the buffer!!!
    int txPort = open(UART_PORT, O_RDWR | O_NOCTTY ); 
    if (txPort == -1)
    {
        printf ("Error no is : %d\n", errno);
        printf("Error opening serial port\n");
        exit(1);
    }
    //set up the uart 
    setUpUart();

    //read in all the lines of a file
    char ch = 1;
    //set up array for tx, the max is 256, so we better not exceed that anyways so using an array of 256 is fine.
    char line[MAX_BYTES_PER_LINE] = {0};
    
    DEBUG_P(Waiting for tx window>>>)
    //this is where we wait until we hit 5 seconds after this code has been called
    while((currentTime - startTime) < DELAY_UNTIL_TX_WINDOW)
    { 
        currentTime = millis();
    }
    DEBUG_P(current Time - Start Time:)
    PRINT_TIME(currentTime - startTime)

    //Send command to put the local radio into pipe mode
    write(txPort, "ES+W22003321\r", 13);
    //Sleep for 1 second to allow time to go into pipe mode
    sleep(1);
    //Transmit command to put the remote radio into pipe mode
    write(txPort, "ES+W23003321\r", 13);
    //Sleep for 1 second to allow time to go into pipe mode
    sleep(1);
    write(txPort, data, COMMAND_SIZE);

    exit(0);
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


void getInput(char * a)
{
	int flag = 0;
	int input, length, dataType, windowsNumber, windowLength, n, i, picture;
    int line;
	long int txTime;
    char message [COMMAND_SIZE];
    a = message;
    while(1){
        printf("1:\tCreate new txWindow.\n"
        "0:\tClose\nInput: ");
        scanf("%d", &input);
        switch(input){
            case 0: return;
            case 1:
                printf("Input time until next window: ");
                scanf("%d", &length);
                printf("Input the length of the window: ");
                scanf("%d", &windowLength);
                printf("Input the data type: ");
                scanf("%d", &dataType);
                printf("Input the picture number: ");
                scanf("%d", &picture);
                printf("Input line to start from:");
                scanf("%d", &line);
                txTime = time(NULL);
                // fprintf(fptr, "%ld,%d,%d,0,%d\n", 
                // txTime, windowLength, dataType, line);
                char temp = 0;
                //4 byte of time stamp
                for(int i = 0; i < 8; i++)
                {
                    temp = length >>8;
                    message[i] = temp;
                }

                //two bytes of window durations
                temp = windowLength >>8;
                message[5] = temp;
                temp = windowLength >>8;
                message[6] = temp;

                //one byte data type
                temp = dataType >>8;
                message[7] = temp;

                //two bytes of picture
                temp = picture >>8;
                message[8] = temp;
                temp = picture >>8;
                message[9] = temp;

                //4 bytes of line number
                for(int i = 0; i < 8; i++)
                {
                    temp = line >>8;
                    message[i + 10] = temp;
                }
                break;
            default:
                return;
        }
    }
}