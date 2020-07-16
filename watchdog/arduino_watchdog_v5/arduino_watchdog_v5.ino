#include<avr/wdt.h>
#include <Wire.h>

//Pin numbers for the input Heartbeat and output to the MOSFET
const int HEARTBEAT = 9;
const int MOSFET = 10;

//Time that the watchdog will wait without input from Pi before shutting off (in milliseconds)
const long PI_CHECK_TIME = 5000;

//Custom delay times (in milliseconds)
const long DELAY1 = 60000;
const long DELAY2 = 120000;
const long DELAY3 = 180000;

long customBootDelay;

bool bootInProgress = false;
bool customBootInProgress = false;

//Standard Boot delay time
const long BOOT_DELAY_TIME = 60000; //120000;

//Event that triggers on an I2C write
void receiveEvent(int howMany){
  //If we are not currently booting
  if(bootInProgress == false && customBootInProgress == false){
    int selection = Wire.read();    // receive byte as an integer
    //Set the custom boot delay to one of the pre-defined delay times, we can make up to 256 custom delays
    switch (selection) {
      case 1:
        customBootDelay = DELAY1;
        customBootInProgress = true;
        break;
      case 2:
        customBootDelay = DELAY2;
        customBootInProgress = true;
        break;
      case 3:
        customBootDelay = DELAY3;
        customBootInProgress = true;
        break;

       //I added this in case we need to dealy for an hour, 6 hours, 12 hours, or even a day. This are last resort times in case of safe mode. 
       case 10: 
       case 60: 
       case 120: 
       case 240:
        customBootDelay = (long) selection * 6000 * 60 * 60;
        customBootInProgress = true;
        break;
        
      default:
        break;
    }
  }
}

//Custom wait function that acts like delay, but does not time out the internal watchdog
void wait(long delayTime){
  long timer_start = millis();
  long timer = millis();
  while(timer_start + delayTime >= timer) {
    wdt_enable(WDTO_8S);
    timer = millis();
    
    Serial.print("Timer start: ");
    Serial.print(timer_start);
    Serial.print("\t\tTimer: ");
    Serial.print(timer);
    Serial.print("\t\tdelay time: ");
    Serial.println(delayTime);
    
    //check for overflow
    if(timer_start > timer + 10){
      Serial.println("Int overflow tripped, resetting timers");
      timer_start = millis();
      timer = millis();
    }
  }
}

//Function returns true if there has been no response from the Pi in PI_CHECK_TIME milliseconds
bool isPiDead(){
  bool exitLoop = false;
  int piState = digitalRead(HEARTBEAT);
  long check_timer_start = millis();
  delay(100);
  long check_timer = millis();
  while(exitLoop == false) {
    check_timer = millis();
    Serial.print("Check timer start: ");
    Serial.print(check_timer_start);
    Serial.print("\t\tCheck timer: ");
    Serial.println(check_timer);

    //check for overflow
    if(check_timer_start > check_timer){
      Serial.println("Int overflow tripped, resetting timers");
      check_timer_start = millis();
      check_timer = millis();
    }
    
    if(piState != digitalRead(HEARTBEAT)){
      exitLoop = true;
      return false;
    }
    if(check_timer_start + PI_CHECK_TIME <= check_timer){
      exitLoop = false;
      return true;
    }
  }
  return true;
}


void setup() {
  wdt_disable();
  
  // initialize pins
  pinMode(MOSFET, OUTPUT);
  pinMode(HEARTBEAT, INPUT);

  //Set MOSFET to low by default
  digitalWrite(MOSFET, LOW);

  Wire.begin(8);                // join i2c bus with address #0x08
  Wire.onReceive(receiveEvent); // Run receiveEvent code when an I2C message is received
}

void loop() {
  wdt_enable(WDTO_8S);
  //If there is a custom boot from the I2C line
  if(customBootInProgress == true){
    //Turn of Pi
    digitalWrite(MOSFET, HIGH);
    Serial.println("Pi is off");
    
    //Delay the custom amount of time
    wait(customBootDelay);
    customBootInProgress = false;

    //Turn on Pi and resume regular booting protocol
    //pi on
    digitalWrite(MOSFET, LOW);
    Serial.println("Pi on");
    bootInProgress = true;
  }
  
  //If we have lost signal from the Pi and are rebooting, or rebooting after a custom boot
  else if(bootInProgress == true){
    wait(BOOT_DELAY_TIME);
    bootInProgress = false;
  }
  
  //No boots are in progress, check the HEARTBEAT pin as normal
  else{
    Serial.println("Checking Pi...");
    bootInProgress = isPiDead();

    //If there was no response, reset the Pi
    if(bootInProgress == true){
      //Code to reboot Pi
      Serial.println("Rebooting Pi");
      //reset pi
      //pi off
      digitalWrite(MOSFET, HIGH);
      Serial.println("Pi is off");
      wait(200);
      //pi on
      digitalWrite(MOSFET, LOW);
      Serial.println("Pi on");
    }
  }
}
