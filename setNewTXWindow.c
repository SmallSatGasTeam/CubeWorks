#include <stdio.h>
#include <stdlib.h>

char command0[] = "date +%s";

int main(int argc, char * argv[])
{
	FILE *fptr;
	fptr = fopen("/home/pi/TXISRData/txWindows.txt","a+");
	int flag = 0;
	int input, length, dataType, windowsNumber, windowLength, n, i;
	long int txTime;

        if(fptr == NULL)
        {
                printf("ERROR WITH FILEPATH\n");
                exit(1);
        } 

	if(argc == 1){
		printf("You are creating custom txWindows. To create multiple at equal"
		" intervals, the usage is: sudo ./setNewTXWindow.c <number of"
		" intervals> <time between each window> <length of each window>" 
		"<data type>\n");

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
					txTime = (long int) time(NULL);
					txTime += length;
					fprintf(fptr, "%ld,%d,%d,0,1\n", 
					txTime, windowLength, dataType);
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
						if(!flag) txTime = (long int) time(NULL);
						txTime += length;
						fprintf(fptr, "%ld,%d,%d,0,1\n", 
						txTime, windowLength, dataType);
						flag = 1;
					}
					break;
				default:
					return 0;
			}
		}
	}
	else if(argc != 5) {
		printf("ERROR. Improper usage.\n"
		"Usage: sudo ./setNewTXWindow.c <number of intervals> "
		"<time between windows> <length of each window> <data type>");
	}
	else {
		n = atoi(argv[1]);
		length = atoi(argv[2]);
		windowLength = atoi(argv[3]);
		dataType = atoi(argv[4]);
		txTime = (long int)time(NULL);

		for(i = 0; n < i; i++){
			fprintf(fptr, "%ld,%d,%d,0,1\n", txTime, windowLength, dataType);
		}
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
	
