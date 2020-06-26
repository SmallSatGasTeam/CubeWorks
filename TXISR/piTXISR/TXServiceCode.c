//#include <unistd.d>
#include <fcntl.h>
#include <termios.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
//Take just the DEBUG line out when your are done debugging and leave debug.h
#define DEBUG
#include "debug.h"

//enable and disable are set up in the make file,
#define ENABLE "./conifPinTXISR"
#define DISABLE "./conifPinTXISRDone"

#define FLAG_FILE "./out.txt" //change this later for the real program
#define FORMAT_FILE "./temp.txt" //this is the file that dallan will creat
#define UART_PORT "/dev/serial0" //this is serial port name, make sure this is correct for the final code

//this sets control of the settings for our serial port
struct termios options;

void setUpUart();


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
void main(int argc,char* argv[])
{

    /////TODO/////
    /*
    *Make a make file that compiles the program and compiles the bash scripts
    *Add in the time check on transmissionWindow 
    *Add in the wait after each transmission 
    *Write the time to the flags file
    *Add in any set up commucation to the radio
    *find the uart name
    *talk to dallan about formatting of both files, where he is going to put the time 
    *   and passing me the transmission window.
    * TEST, UART, and the bash commands
    */
    int numOfRecords = argv[1];
    int dataType = argv[2];
    long transmissionWindow = argv[3];

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

    //open the serial ports
    int txPort = open(UART_PORT, O_RDWR | O_NOCTTY ); 
    if (txPort == -1)
    {
        printf ("Error no is : %d\n", errno);
        printf("Error description is : %s\n",strerror(errno));
        exit(1);
    }
    //set up the uart 
    setUpUart();

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
        //this line of code sends things out on the tx line
        write(txPort, line, charCount);
        if(ch == 10 && ch != EOF)
        {
            ch = fgetc(txFile);
        }
    } 

    //give control of the port back to linuxs
    int disable = system(DISABLE);
    //if we fail reboot
    if(disable == -1) 
    {
        DEBUG_P(Failed to release tx uart pin)
        exit(1);
    } 
}

/*******************************************************************************************
 * setUpUart
 * this func sets up the uart commincation for us so everything works nicely
 *******************************************************************************************/
void setUpUart()
{
    //set the baud rate, it is the number with a b infornt of it ex 115200 -> B115200
    cfsetspeed(&options, B115200);

    //set up the number of data bits
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8;
}