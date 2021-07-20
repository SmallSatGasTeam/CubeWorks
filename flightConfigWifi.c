#include <stdio.h>
#include <stdlib.h>

char cammand0 [] = "sudo crontab -l >> crontab_new ; echo @reboot sudo /usr/bin/tvservice -o >> crontab_new ; sudo crontab crontab_new ; rm crontab_new";
char cammand1 [] = "sudo cat /boot/config.txt >> config_temp ; sudo echo dtparam=act_led_trigger=none >> config_temp";
char cammand2 [] = "sudo echo dtparam=act_led_activelow=on >> config_temp ";
char cammand5 [] = "sudo cp config_temp /boot/config.txt ; rm config_temp";

/*************************************************************************
 * This is the code that will set the pi into the power saving options we 
 * want to use.
 * NOTE: This does not dispable wifi as well, this is for testing finial
 * configuration
 ************************************************************************/
void main()
{
    system(cammand0);
    system(cammand1);
    system(cammand2);
    system(cammand5);
    system("sudo reboot");
}

//this code will update all the code bases 
//Written by Shawn