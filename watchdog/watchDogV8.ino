 //Includes deep sleep functionality
#include "LowPower.h"
//this lets us save to flash memory so we don't lose the no heart beet count on reboot
#include <EEPROM.h>

//Pin numbers for the input Heartbeat and output to the MOSFET
const int HEARTBEAT = 9;
const int MOSFET = 10;
const int MAX_REBOOTS = /*5; */ 100;

//Time that the watchdog will wait without input from Pi before shutting off (in milliseconds)
const long PI_CHECK_TIME = 4000; //30000;

/*
//Custom delay times (in milliseconds)
const long DELAY1 = 60000;
const long DELAY2 = 120000;
const long DELAY3 = 180000;
*/

const long twentyfour_HOUR_REBOOT = 86400000;
const long twentyfour_Hour_Window = 30000;

int noHeartbeatBootCount = 0;

bool bootInProgress = false;

//Standard Boot delay time
const long BOOT_DELAY_TIME = 2000;//120000;

//Time the watchdog keeps the pi off
const long PI_OFF_TIME = 5000;

//Custom wait function that acts like delay, but checks for int overflow, and puts the arduino into low power mode for 1 second
void wait(long delayTime){
  long timer_start = millis();
  long timer = millis();
  while(timer_start + delayTime >= timer) {
    timer = millis();
    
    //check for overflow
    if(timer_start > timer + 10){
     // Serial.println("Int overflow tripped, resetting timers");

      delayTime -= (2147483647 - timer_start); //length of a long minus the timer start. Gives the time we already waited and subtracts that from the delay variable 
      
      
      timer_start = millis();
      timer = millis();
    }

    //go to low power for 1 second
    //LowPower.powerDown(SLEEP_1S, ADC_OFF, BOD_OFF);
    delay(1000);  
  }
}

//Function returns true if there has been no response from the Pi in PI_CHECK_TIME milliseconds
bool isPiDead(){
  bool exitLoop = false;

  bool reboot24 = false;

  int piState = digitalRead(HEARTBEAT);
  long check_timer_start = millis();
  delay(100);
  long check_timer = millis();
  while(exitLoop == false) {
    check_timer = millis();
    //Serial.print("Check timer start: ");
    //Serial.print(check_timer_start);
    //Serial.print("\t\tCheck timer: ");
    //Serial.println(check_timer);
    //Serial.print("Pi state:");
    //Serial.println(piState);

    //check for overflow
    if(check_timer_start > check_timer){
      //Serial.println("Int overflow tripped, resetting timers");
      check_timer_start = millis();
      check_timer = millis();
    }
    
    if(piState != digitalRead(HEARTBEAT)){
      //this will leave the loop so that we can check if it is a 24 hour reset
      noHeartbeatBootCount = 0;
      EEPROM.update(0, noHeartbeatBootCount);
      //Serial.println("Hertbeat detected, Resetting boot count to 0");
      exitLoop = true;
    }
    if(check_timer_start + PI_CHECK_TIME <= check_timer){
      noHeartbeatBootCount++;
      EEPROM.update(0, noHeartbeatBootCount);
      //Serial.println(EEPROM.read(0));
      //Serial.print("Boot count without hearing a heartbeat: ");
      //Serial.println(noHeartbeatBootCount);
      exitLoop = false;
      return true;
    }

    reboot24 = twentyfour_Hour_Reboot(check_timer);
    if(reboot24 == true){
      return reboot24;
    }

    //Put arduino into low power mode for 1 second
    delay(1000);
    
  }

  //check if it is a 24 hour reset
  return twentyfour_Hour_Reboot(check_timer);
}


/**************************************************************
 * this is what handelst he 24 hour reboot, it will 
 * returns weather it is time to reboot or not
 * this will always happen
 *************************************************************/

bool twentyfour_Hour_Reboot(long currentSystemTime)
{
  //Serial.println("Checking for 24 hr reboot");
  if((currentSystemTime % twentyfour_HOUR_REBOOT >= twentyfour_HOUR_REBOOT - twentyfour_Hour_Window) && (currentSystemTime % twentyfour_HOUR_REBOOT <= twentyfour_HOUR_REBOOT) && (currentSystemTime > 100))
  {
    //Serial.println("Found a 24 hour reboot, executing order 66");
    return true;
  }
  else
  {
    //Serial.print("No reboot found. Current system time: ");
    //Serial.print(currentSystemTime);
    //Serial.print("\t\t Reboot: ");
    //Serial.print(twentyfour_HOUR_REBOOT);
    //Serial.print("\t\t Time mod reboot: ");
    //Serial.println(currentSystemTime % twentyfour_HOUR_REBOOT);
    return false;
  }
}

void boot_delay(){
    for(int i = 0; i < 3/*15*/; i++){
      LowPower.powerDown(SLEEP_8S, ADC_OFF, BOD_OFF);  
    }
}


void setup() {

  // initialize pins
  pinMode(MOSFET, OUTPUT);
  //pinMode(LED_BUILTIN,OUTPUT);
  pinMode(HEARTBEAT, INPUT);

  //Set MOSFET to low by default
  digitalWrite(MOSFET, LOW);

  //This is a work around to make the dual booting functional. In case the Arduino is reset when the Pi rebots, the Arduino will wait for the Boot time before beginning watchdog operations
  //This puts the arduino into deep sleep for 120 seconds. The longest we can put it into deep sleep is 8 seconds.

  boot_delay();
}

void loop() {
//  wdt_enable(WDTO_8S);
//the boot count is save in possition zero 
  noHeartbeatBootCount =  EEPROM.read(0);
  
  //If we have lost signal from the Pi and are rebooting, or rebooting after a custom boot
  if(bootInProgress == true){
    //wait(BOOT_DELAY_TIME);
    boot_delay();
    bootInProgress = false;
  }
  
  //No boots are in progress, check the HEARTBEAT pin as normal
  else if (MAX_REBOOTS >= noHeartbeatBootCount){
    //Serial.println("Checking Pi...");
    bootInProgress = isPiDead();

    //If there was no response, reset the Pi
    if(bootInProgress == true){
      //save the noHeartbeatBootCount into the eeprom memory
      //EEPROM.write(0, noHeartbeatBootCount);
      //Code to reboot Pi
     // Serial.println("Rebooting Pi");
//      Serial.print("Boot count without hearing a heartbeat: ");
      
      //reset pi
      //pi off
      digitalWrite(MOSFET, HIGH);
//      Serial.println("Pi is off");
      //Busy wait for 1 second so we don't loose control of the MOSFET pin
      delay(1000); 
      //pi on
      digitalWrite(MOSFET, LOW);
//      Serial.println("Pi on");
    }
  }
  else 
  {
    //we are just going to keep checking to see if the pi comes back on, should we ever run into the case were we max out the reboots
      isPiDead();
     // boot_delay();
      if(twentyfour_Hour_Reboot(millis()) == true){
      
        //reset pi
        //pi off
        digitalWrite(MOSFET, HIGH);
        Serial.println("Pi is off");
        //Busy wait for 1 second so we don't loose control of the MOSFET pin
        wait(1000); 
        //pi on
        digitalWrite(MOSFET, LOW);
        Serial.println("Pi on");
        boot_delay();
        //wait(BOOT_DELAY_TIME);
      }
  }
}
