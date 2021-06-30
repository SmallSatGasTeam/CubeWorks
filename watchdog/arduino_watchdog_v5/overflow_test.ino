#include<avr/wdt.h>

//Custom wait function that acts like delay, but does not time out the internal watchdog
void wait(long delayTime){
  long timer_start = millis() + 2147453000;
  long timer = millis() + 2147453000;
  while(timer_start + delayTime >= timer) {
    wdt_enable(WDTO_8S);
    timer = millis() + 2147453000;

    //digitalWrite(LED, HIGH);
    Serial.print("Timer start: ");
    Serial.print(timer_start);
    Serial.print("\t\tTimer: ");
    Serial.print(timer);
    Serial.print("\t\tdelay time: ");
    Serial.println(delayTime);
    
    //digitalWrite(LED, LOW);
    
    //check for overflow
    if(timer_start > timer + 10){
      Serial.println("Int overflow tripped, resetting timers");

      //Experimental code, needs testing 
      delayTime -= (2147483647 - timer_start); //length of a long minus the timer start. Gives the time we already waited and subtracts that from the delay variable 
      
      
      timer_start = millis();
      timer = millis();
    }
  }
}

void setup() {
  wdt_disable();
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
  wait(60000);
  Serial.println("Wait function ended.");
}
