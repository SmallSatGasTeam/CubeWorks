#include <stdio.h>
#include <stdlib.h>

int main(int argc, char * argv[]){
    int output;

    if(argc != 2){
        printf("Incorrect usage.\n");
        exit(1);
    }

    FILE * file;
    file = fopen(argv[1], "w+");


    if(file == NULL){
        printf("Failed to open file.\n");
    }
    else
    fclose(file);

    return 0;
}