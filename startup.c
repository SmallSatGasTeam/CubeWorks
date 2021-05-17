#include <stdio.h>
#include <stdlib.h>

int main(void){
    FILE *lastBase;
    int codeBase;
    int i;

    printf("About to open lastBase.\n");

    lastBase = fopen("lastBase.txt", "r");
    if(lastBase == NULL){
        codeBase = 0;
        printf("Failed to find the file.\n");
    }
    else {
        codeBase = (int) getc(lastBase) % 48;
        fclose(lastBase);
    }

    if(codeBase >= 4) codeBase = 0;
    else codeBase++;

    lastBase = fopen("lastBase.txt", "w");
    fprintf(lastBase, "%d", codeBase);
    fclose(lastBase);

    //I needed a comment in here so I can push
    switch(codeBase) {
        case 0: printf("Running code base 0.\n"); system("cd CubeWorks0/tests\nsudo python3 testMainFlightLogicNOTSub.py");
            break;
        case 1: printf("Running code base 1.\n"); system("cd CubeWorks1/tests\nsudo python3 testMainFlightLogicNOTSub.py");
            break;
        case 2: printf("Running code base 2.\n"); system("cd CubeWorks2/tests\nsudo python3 testMainFlightLogicNOTSub.py");
            break;
        case 3: printf("Running code base 3.\n"); system("cd CubeWorks3/tests\nsudo python3 testMainFlightLogicNOTSub.py");
            break;
        case 4: printf("Running code base 4.\n"); system("cd CubeWorks4/tests\nsudo python3 testMainFlightLogicNOTSub.py");
            break;
        default: printf("Running code base 0.\n"); system("cd CubeWorks0/tests\nsudo python3 testMainFlightLogicNOTSub.py");
            break;
    }

    return 0;
}