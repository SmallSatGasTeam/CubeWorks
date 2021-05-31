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

//enable and disable are set up in the make file,
#define ENABLE "./configPinsTXISR"
#define DISABLE "./configPinsTXISRDone"

#define FLAG_FILE "/home/pi/TXISRData/flagsFile.txt" //change this later for the real program
#define FORMAT_FILE "../data/txFile.txt" //this is the file that dallan will creat 
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

//NOTE: becasue of how we have to set the boud rate I cannot use a define for it in ceritian places, just do a contrl f and look for BOUD_RATE
//it is place next to every place that the boud rate is used, you also need to change the define as it is used as well.
//NOTE: this boud rate (9600) is the radio speed. We talk to it with a diffrent speed, in other words the 9600 is our divisor for the delay
#define BOUD_RATE 9600

int changeCharToInt(char a);

//this sets control of the settings for our serial port
struct termios options;

void setUpUart();
char convertCharToHex (char lowByte, char highByte);
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
    /////TODO/////
    /*
    *debug the time check on transmissionWindow 
    *debug the wait after each transmission 
    *Write the time to the flags file
    *Add in any set up commucation to the radio
    * TEST, UART, and the bash commands
    */
    intmax_t startTime = millis();
    intmax_t currentTime = millis();
    intmax_t startTimeTX = 0;
    intmax_t currentTimeTX = 0;
    char data[64];
    DEBUG_P(Made it past all of these variable instantiations)
    //gather user input
    getInput(&data);
    int dataType;
    if(argc == 2) {
        printf("About to convert char to int: %s %c\n", argv[1], *argv[1]);
        dataType = changeCharToInt(*argv[1]);
        printf("DataType: %d\n", dataType);
    }
    else dataType = changeCharToInt(127);
    //DEBUG_P(Made it past the problem spot)
    int transmissionWindow = 0;
    char sendingData[(MAX_NUM_OF_DATA_TYPES / 2)] = {0}; 


    FILE *txFile;
    txFile = fopen(FORMAT_FILE, "r");
    if (txFile == NULL)
    {
        //if we fail exit
        DEBUG_P(Failed to open file)
        exit(1);
    }

    FILE *recordFile;
    recordFile = fopen(FLAG_FILE, "r+");
    if (recordFile == NULL)
    {
        //if we fail exit
        DEBUG_P(Failed to open the flags file)
        exit(1);
    }

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

    currentTime = millis();
    DEBUG_P(currentTime - startTime)
    DEBUG_P(\nSending>>>)

    int charCount = 0;
    int end = 0;
    int charTimeCount = 0;
    char chl = '0';
    for(int i = 0; i < MAX_BYTES_PER_LINE; i++){
        line[i] = '0';
    }

    line[charCount++] = 
    line[charCount++] = 

    exit(0);
     //give control of the port back to linuxs
    //  int disable = system(DISABLE);
    //  //if we fail reboot
    //  if(disable != 0) 
    //  {
    //      DEBUG_P(Failed to release tx uart pin)
    //      exit(1);
    //  } 
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

/*******************************************************************************************
 * setUpUart
 * this func will convert a char in to an int (works for 0 though 9 and a - f)
 * if it fails to convert the vaule it exits the program and sends an error message.
 *******************************************************************************************/
int changeCharToInt(char a)
{
    switch(a)
    {
        //use assci table to decode this part of the code
        case '0':
            return 0;
        case '1':
            return 1;
        case '2':
            return 2;
        case '3':
            return 3;
        case '4':
            return 4;
        case '5':
            return 5;
        case '6':
            return 6;
        case '7':
            return 7;
        case '8':
            return 8;
        case '9':
            return 9;
        case 'a':
            return 10;
        case 'b':
            return 11;
        case 'c':
            return 12;
        case 'd':
            return 13;
        case 'e':
            return 14;
        case 'f':
            return 15;
        default :
            {
                DEBUG_P(invaild data type)
                PRINT_DEBUG_c(a)
                printf("A in int form: %d\n", a);
                return 127;
            }
    }
}
/*******************************************************************************************
 * Convertto hex
 * this func will convert a char in to hex 
 * if it fails to convert the vaule it exits the program and sends an error message.
 * it returns the int value
 *******************************************************************************************/
char convertCharToHex (char lowByte, char highByte)
{
    //convert to ints
    char low = changeCharToInt(lowByte);
    char high = changeCharToInt(highByte);
    //shift high and add it to low.
    char new = 127;
    if(!((low == 127) || (high == 127))) {
        char new = low + (high << 4);
    }
    return new;
}

void getInput(int * a)
{
    FILE *fptr;
	fptr = fopen("/home/pi/TXISRData/txWindows.txt","a+");
	int flag = 0;
	int input, length, dataType, windowsNumber, windowLength, n, i, line, picture;
	long int txTime;

    if(fptr == NULL)
    {
            printf("ERROR WITH FILEPATH\n");
            exit(1);
    } 

    while(1){
        printf("1:\tCreate single new txWindow.\n"
        "2:\tCreate multiple txWindows with varying time inbetween.\n"
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
                length += (int) txTime;
                *a = (int) txTime + length;
                a++;
                *a = windowLength;
                a++;
                *a = dataType;
                a++;
                *a = picture;
                a++;
                *a = line;
                break;
            case 2:
                printf("Warning, this one has not been edited yet and is not working.\n");
                printf("Input the number of windows to create: ");
                scanf("%d", &n);
                for(i = 0; i < n; i++){
                    printf("Window %d.\n", i+1);
                    printf("Input time until next window: ");
                    scanf("%d", &length);
                    printf("Input the length of the window: ");
                    scanf("%d", &windowLength);
                    printf("Input the data type: ");
                    scanf("%d", &dataType);
                    printf("Input the line number: ");
                    scanf("%d", &line);
                    if(!flag) txTime = (long int) time(NULL);
                    txTime += length;
                    fprintf(fptr, "%ld,%d,%d,0,%d\n", 
                    txTime, windowLength, dataType, line);
                    flag = 1;
                }
                break;
            default:
                return;
        }
    }

	fclose(fptr);
}