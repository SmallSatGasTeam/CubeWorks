#include <unistd.d>
#include <fcntl.h>
#include <termios.h>
#include <stdio.h>
#include <stdlib.h>
#define ENABLE "conifPinTXISR"
#define DISABLE "conifPinTXISRDone"

void main(void)
{
    printf("echo Hello\n");
    int ret = system("echo hello world");
    if(ret == 0) printf("It worked\n");
    else if (ret == -1) printf("didn't work\n");
    printf("The value of ret: %d\n", ret);
}