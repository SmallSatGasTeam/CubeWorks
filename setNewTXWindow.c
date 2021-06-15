#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/* This code provides a simple way to feed a transmission window into txWindows.txt while running the main flight logic. */

char command0[] = "date +%s";

int main(int argc, char * argv[])
{
	FILE *fptr;
	fptr = fopen("/home/pi/TXISRData/txWindows.txt","a+");
	int flag = 0;
	int input, dataType, windowsNumber, windowLength, n, i, line, pic, length;
	long int Time;
	time_t txTime;

        if(fptr == NULL)
        {
                printf("ERROR WITH FILEPATH\n");
                exit(1);
        } 

	if(argc == 1){
		printf("You are creating custom txWindows. To create multiple at equal"
		" intervals, the usage is: sudo ./setNewTXWindow.c <number of"
		" intervals> <time between each window> <length of each window>" 
		"<data type> <picture number> <line number>\n");

		while(1){
			printf("1:\tCreate single new txWindow.\n"
			"2:\tCreate multiple txWindows with varying time inbetween.\n"
			"0:\tClose\nInput: ");
			scanf("%d", &input);
			switch(input){
				case 0: return 0;
				case 1:
					printf("Input time until next window: ");
					scanf("%d", &length);
					printf("Input the length of the window: ");
					scanf("%d", &windowLength);
					printf("Input the data type: ");
					scanf("%d", &dataType);
					printf("Input the picture number:");
					scanf("%d", &pic);
					printf("Input line to start from:");
					scanf("%d", &line);
					txTime = time(NULL);
					Time = (long int) txTime + length;
					fprintf(fptr, "%ld,%d,%d,%d,%d\n", 
					Time, windowLength, dataType, pic, line);
					break;
				case 2:
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
						printf("Input the picture number:");
						scanf("%d", &pic);
						printf("Input the line number: ");
						scanf("%d", &line);
						if(!flag){
							txTime = time(NULL);
							Time = (long int) txTime;
						}
						Time += length;
						fprintf(fptr, "%ld,%d,%d,%d,%d\n", 
						Time, windowLength, dataType, pic, line);
						flag = 1;
					}
					break;
				default:
					return 0;
			}
		}
	}
	else if(argc == 7) {
		n = atoi(argv[1]);
		length = atoi(argv[2]);
		windowLength = atoi(argv[3]);
		dataType = atoi(argv[4]);
		txTime = time(NULL);
		Time = (long int) txTime;
		pic = atoi(argv[5]);
		line = atoi(argv[6]);

		for(i = 0; i < n; i++){
			Time += length;
			printf("Creating window %d: %ld,%d,%d,%d,%d \n", 
				i+1, Time, windowLength, dataType, pic, line);
			fprintf(fptr, "%ld,%d,%d,%d,%d\n", 
				Time, windowLength, dataType, pic, line);
		}
	}
	else {
		printf("ERROR. Improper usage.\n"
		"Usage: sudo ./setNewTXWindow.c <number of intervals> "
		"<time between windows> <length of each window> <data type>"
		" <picture number> <line number>\n");
	}

	// system(command0);
	// printf("Please enter the number above: ");
	// scanf("%d",&txTime);
	// txTime += 40;
	// fprintf(fptr, "%d,30,0,0,00000001\n", txTime);
	// txTime += 45;
	// fprintf(fptr, "%d,30,0,0,00000001\n", txTime);

	// txTime += 45;
	// fprintf(fptr, "%d,30,0,0,00000001\n", txTime);

	fclose(fptr);
}
	
