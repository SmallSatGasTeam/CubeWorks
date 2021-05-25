#include <stdio.h>
#include <stdlib.h>

char command0[] = "date +%s";

void main()
{
        FILE *fptr;
        fptr = fopen("/home/pi/TXISRData/txWindows.txt","a+");
	int txTime;

        if(fptr == NULL)
        {
                printf("ERROR WITH FILEPATH");
                exit(1);
        } 

	system(command0);
	printf("Please enter the number above: ");
	scanf("%d",&txTime);
	txTime += 40;

	fprintf(fptr, "%d,30,0,0,00000001", txTime);
	fclose(fptr);
}
	
