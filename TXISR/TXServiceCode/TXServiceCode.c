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

#define FLAG_FILE "/home/pi/TXISRData/flagsFile.txt" //change this later for the real program
#define FORMAT_FILE "../data/txFile.txt" //this is the file that dallan will creat 
#define UART_PORT "/dev/serial0" //this is serial port name, make sure this is correct for the final code

//this is our time delay
#define DELAY_tx 120

//this defines are for the data types
#define MAX_BYTES_PER_LINE 256
#define MAX_NUM_OF_DATA_TYPES 5
#define DELAY_UNTIL_TX_WINDOW 0
#define PHOTO_TYPE 3
#define TIME_DEVISOR ':'

//NOTE: Because of how we have to set the boud rate, I cannot use a define for it in certain places, just do a ctrl-f and look for BOUD_RATE
//it is place next to every place that the boud rate is used, you also need to change the define as it is used as well.
//NOTE: this boud rate (9600) is the radio speed. We talk to it with a different speed, in other words the 9600 is our divisor for the delay
#define BOUD_RATE 9600

int changeCharToInt(char a);

//this sets control of the settings for our serial port
struct termios options;

void setUpUart();
char convertCharToHex (char lowByte, char highByte);

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
    DEBUG_P(Made it past all of these variable instantiations)
    //gather user input
    int dataType;
    int writeFlag;
    if(argc == 2) {
        printf("About to convert char to int: %s %c\n", argv[1], *argv[1]);
        dataType = changeCharToInt(*argv[1]);
        printf("DataType: %d\n", dataType);
    }
    else dataType = changeCharToInt(-1);
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

    //this is where we will store the last transmission
    //5 data types
    int flags[MAX_NUM_OF_DATA_TYPES];
    //pop the data types
    DEBUG_P(opening file)
    //NOTE: WE HAVE TO MAKE THE FLAGS FILE RIGHT OR WE WILL GET SYSTEM FAILURE.
    size_t lineSize;
    for (int i =0; (i < MAX_NUM_OF_DATA_TYPES) & !(feof(recordFile)); i++)
    {
        fscanf(recordFile, "%ld", &flags[i]);
        PRINT_TIME(flags[i]);
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
    int lineNumber = 0;
    //get tx time
    if(!feof(txFile)){
        fscanf(txFile, "%d", &transmissionWindow);
    }
    PRINT_DEBUG(transmissionWindow)
    if(!feof(txFile)){
        char dumb = fgetc(txFile);
        PRINT_DEBUG_c(dumb);
    }
    currentTime = millis();
    
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

    while(!feof(txFile))
    {
       //this checks the transmission window
        currentTime = millis();
        //break if we have passed the tx window
        if((currentTime - startTime) > transmissionWindow) 
        {
            PRINT_TIME(currentTime - startTime)
            DEBUG_P(\nInvaild time Ending>>>)
            break;
        }

        
        DEBUG_P(current Time - Start Time:)
        PRINT_TIME(currentTime - startTime)
        DEBUG_P(\nSending>>>)
        //get the size of each line in the file
        int charCount = 0;
        int end = 0;
        char chl = '0';
        for (int i = 0; i < MAX_BYTES_PER_LINE; i++)
        {
            line[i] = '0';
        }

        do {
            if(feof(txFile)) break;
            ch = fgetc(txFile);
            //this collects the time stamp

            lineNumber += changeCharToInt(ch);
            printf("Finding the timestamp: ");
            PRINT_DEBUG_c(ch)

            if (ch == TIME_DEVISOR)
            {
                end = 1;
            }
        } while(!end && !feof(txFile));

        // DEBUG_P(Found a colon and leaving the first loop)

        while((ch != '\n') && (!feof(txFile)) && (chl != '\n'))
        {
            char temp;
            //if(feof(txFile)) break;
            //save all the data in that line
            //this if lets us not send the line number if this is a photo file
            ch = fgetc(txFile);
            chl = fgetc(txFile);
            /*If we hit a new line character, break out of the loop so we don't
            ever run the code beneath it*/
            if((ch == '\n') || (chl == '\n')){
                break;
            }
            else temp = convertCharToHex(chl, ch);
            //If we receive a bad value
            if(temp == -1){
                char trash[256];
                fscanf(txFile, "%s", trash); //We pull the rest of the line and throw it away

                //Then empty the array
                for(int i = 0; i < 256; i++){
                    line[i] = 0;
                }

                break;  //Then break from the loop
            }
            else {
                line[charCount++] = temp;
            }
        }
        
        // DEBUG_P(leaving loop)

        if((ch == '\n') || (feof(txFile)) || (chl == '\n'))
        {
            //transmit the data
            #ifdef DEBUG
                for(int i = 0; i < charCount; i++)
                {
                    printf("%X", line[i]);
                    if (line[i] == 0) {
                        PRINT_DEBUG_CHAR('0')
                    }
                }
                PRINT_DEBUG_CHAR('\n')
            #endif
            //this line of code sends things out on the tx line
            //start the transmition time
            startTimeTX = millis();
            currentTimeTX = 0;
            write(txPort, line, charCount);
            //this will let us print to the file
            int written = 0;
            //this stores the last sent data time
            if(!(dataType == -1)){
                flags[dataType] = lineNumber;
            }
            PRINT_LONG(flags[dataType])
            //delay the right amount of time for the radio, 120 millisecod + the amount of bytes / by the boud_rate, in almost 
            //cause this will make no diffrence. 
            while((currentTimeTX - startTimeTX) < DELAY_tx)
            { 
                currentTimeTX = millis();
                if(!written)
                {
                    //delete the existing data
                    //fclose(recordFile);
                    if (recordFile = fopen(FLAG_FILE,"w"))
                    {
                        //if succesfull we will print it and set the written to true else we will try again.
                        //reprint it
                        //print the last sent time
                        for(int g = 0; g < MAX_NUM_OF_DATA_TYPES; g++)
                        {
                            fprintf(recordFile, "%ld\n", flags[g]);
                        }
                        //set written to true
                        written = 1;
                    }
                    //if we fail recreate the file
                    else
                    {
                        remove(FLAG_FILE);
                        //recreate the file
                        recordFile = fopen(FLAG_FILE,"w");
                        for(int g = 0; g < MAX_NUM_OF_DATA_TYPES; g++)
                        {
                            fprintf(recordFile, "%ld\n", flags[g]);
                        }
                        //set written to true
                        written = 1;
                    }
                    //delete the existing data
                    fclose(recordFile);
                }
                sleep(DELAY_tx/1000);
            }
            charCount = 0;
            DEBUG_P(TX end Time: )
            PRINT_TIME(currentTimeTX)
            DEBUG_P(TX end start Time: )
            PRINT_TIME(startTimeTX)
            DEBUG_P(Delta T: )
            PRINT_TIME(currentTimeTX - startTimeTX)
        
        }
        
    } 
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
                return -1;
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
    char new = -1;
    if(!((low == -1) || (high == -1))) {
        new = low + (high << 4);
    }
    return new;
}
