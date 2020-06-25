//This is the latest addition of the watchdog code, it only has the build-in heart beet nothing else.
//beetle doesn't work well with the watchdog protocol. To be specific, the watchdog doesn't work 
//well with the beetle's boot loader. It will cause an infinite loop. The best way around this 
//is to disable the watchdog for the void setup function and then use it within the void loop. 
//This is the main difference between the adruinoTap2 and this program the adriunoTapb1_finial. 
//
///////////////////////////////////////////////////////////////////////////////////////////////////
//sudo code
//
//disable watchdog
//turn on pi
//enter void loop/ turn on watchdog
//wait for pi input
//if pi delays more then 4 seconds rest
//else rest watchdog
//repet void loop
//
/////////////////////////////////////////////////////////////////////////////////////////////////
//Compile instructions:
//
//Important Note: make sure to download the Arduino ide from the website the app doesn't work
//
//Note:  If the beetle will not come up on your port. Try unplugging it
//then try resting the board, then try resting your computer. If none of that works, try holding
//the rest button and then uploading the code and releasing the reset button
//
//Note: Each beetle has a unique reset button so make sure to look it up online! If you hold the
//wrong pins you can end your board. RIP
///////////////////////////////////////////////////////////////////////////////////////////////////
//Note: the kill switch has not yet been built into the code.
//////////////////////////////////////////////////////////////////////////////////////////////////

//include the wd proticol
#include<avr/wdt.h>
#include <Wire.h>

//the  button
#define BUTTON 9
//MOSFIT pin, make sure not to use the #define function here. The #define actually repalces code in 
//beetle and this will cause the digital pin not to initialize incorrectly. 
const int MOSFIT = 10;
//The pi delay const
#define PI_CHECK 4000

//pre-programmed delay constants. The Pi will select one of these delays to turn off the arduino
#define DELAY1 60000
#define DELAY2 120000
#define DELAY3 180000

unsigned long bootCustomWait = 1000;
bool customBootInProgress = false;

//set LED to high
const int LED = 13;
unsigned long bootLongWait = 120000;
bool bootInProgress = false;
bool longWait = false;
long time1 = 0;
long time2 = 0;

void setup() 
{
 //IMPORTANT NOTE: Make sure watchdog is disabled for this part of the code, if not the code
 //will compile and run. However, after the watchdog resets for the first time the beetle 
 //will no longer run. The beetle will get caught in an infinite loop. At that point you 
 //need to hold the rest pins upload the sketch and then release the reset pins. You have 
 //to manually break the loop. 
 wdt_disable();

 //set up the pins
 pinMode(MOSFIT, OUTPUT);
 pinMode(BUTTON, INPUT);
 pinMode(LED, OUTPUT);

 //turns the pi on
 digitalWrite(MOSFIT, LOW);

 //Turn on led so that we can see the beetle working
 digitalWrite(LED, HIGH);

  Wire.begin(8);                // join i2c bus with address #0x08
  Wire.onReceive(receiveEvent); // register event
}

void loop() 
{  
  //This is where you want to enable the watchdog, just be careful not to set the frequency too low. 
  //If it does get set too low you will have to hold the pins and then upload a new sketch. This will
  //take several tries as it is a timing game. 
  //Note: The wdt_enable does reset the watchdog timer. 
  wdt_enable(WDTO_8S);
  //if we are not waiting on a boot prosses
  if(!longWait)
  {
    Serial.println("Not waiting on a boot process");
    //call the watchdog protocol, this is taken from the adruinoTap2 code.
    bool Reset = watchdogProtocol();
    Serial.print("Reset Boolean: ");
    Serial.println(Reset);
  
    //call the turn fuction
    turn(Reset, &bootInProgress);
    time1 = millis();
  }

  if(customBootInProgress)
  {
    Serial.print("Custom Boot in progress, delay: ");
    Serial.println(bootCustomWait);
    time2 = millis();
    longWait = wait(&time1, &time2, bootCustomWait);
    customBootInProgress = longWait;
  }
  
  //if we are then keep checking our time delay. 
  if(bootInProgress)
  {
    Serial.println("Boot in progress");
    time2 = millis();
    longWait = wait(&time1, &time2, bootLongWait);
    bootInProgress = longWait;
  }
  
}

void receiveEvent(int howMany){
  //If we are not currently booting
  if(bootInProgress == false && customBootInProgress == false){
    int selection = Wire.read();    // receive byte as an integer
    //Set the custom boot delay to one of the pre-defined delay times, we can make up to 256 custom delays
    switch (selection) {
      case 1:
        bootCustomWait = DELAY1;
        turn(false, &customBootInProgress);
        break;
      case 2:
        bootCustomWait = DELAY2;
        turn(false, &customBootInProgress);
        break;
      case 3:
        bootCustomWait = DELAY3;
        turn(false, &customBootInProgress);
        break;

       //I added this in case we need to dealy for an hour, 6 hours, 12 hours, or even a day. This are last resort times in case of safe mode. 
       case 10, case 60, case 120, case 240:
          long newDealy = (long) selection * 6000 * 60 * 60;
          customBootInProgress = newDealy;
          turn(false, &customBootInProgress);
        break;
        
      default:
        break;
    }
  }
}

bool watchdogProtocol()
{ //set timer 
  long timer = millis();

  //set the tiem_check bool to true
  bool time_check = true;

  //set the watchdog bool to false if it remains unchanged it will reset the pi
  bool W_D_PI = false;
  
  //this code runs so that we can see the board is working
  //read the button
  int buttonState = digitalRead(BUTTON);
  Serial.println(buttonState);  

  //record the time that we start the loop
  long time_actual = millis();

  Serial.println("Entering time_check loop");
  //if the PI state is HIGH then it has sent the heartbeat and we reset the count, if not we continue adding to time_actual until we exceed 4,000 in which case the pi will be reset. 
  while(time_check == true)
  {
    //get time actual
    long time_actual = millis();

    /*
    Serial.print("Timer: ");
    Serial.print(timer);
    Serial.print("\t\tTime_actual: ");
    Serial.println(time_actual);
     */

    //check for int overflow 
    //NOTE: this func takes small, big, I had it back words I think that might have been our problem. 
    intOverflow(&timer, &time_actual);
    
    //this logic test is the timer 
    if(PI_CHECK > time_actual - timer)
    {
     time_check = true;
    }
    else
    {
      time_check = false;
    }
   

   //check to see if in what condition the button is in
   //if it is LOW we break the loop
   if(buttonState == LOW)
   {
    while(buttonState == digitalRead(BUTTON)){
        //Serial.println("Waiting for Pi response");
    };
    Serial.println("Pi is alive");
    //set the pi watch dog to true
    W_D_PI = true;
    //break the while loop
    time_check = false;
   } 
   else
   {
    //read the button
    buttonState = digitalRead(BUTTON);
   }
  }
  return W_D_PI;
}

//this fuc reboots the pi
void turn(bool check, bool *startBoot)
{
  if(check == false)
  {
    Serial.println("Rebooting Pi");
    //reset pi
    //pi off
    digitalWrite(MOSFIT, HIGH);
    ///BEN I Think that these delays are tripping the beetle internal watchdog, i think we should go over one second and we should just use the wait func instead of delay
    delay(1000);
    //pi on
    digitalWrite(MOSFIT, LOW);
    ///BEN I Think that these delays are tripping the beetle internal watchdog, i think we should go over one second and we should just use the wait func instead of delay
    delay(1000);
    Serial.println("Pi is rebooted");
    *startBoot = true;
  }
}


//this method quick for int overflow to make sure that the clock does not exceed the long int limit
//takes small big
void intOverflow(long *time1, long *time2)
{
  //check for over flow
  if (*time1 > *time2)
  {
    Serial.println("Int overflow tripped, resetting timers");
    //if so delay one second and reset the times
    delay(10);
    *time1 = millis();
    *time2 = millis();
  }
}

//this method turns the pi off
void OFF(void)
{
  digitalWrite(MOSFIT, HIGH);
}

//this is a custom wait function that we will use to aviod the problem of the watchdog timming out.
bool wait(long *time1, long *time2, unsigned long delayTime)
{
    Serial.print("Timer1: ");
    Serial.print(*time1);
    Serial.print("\t\tTimer2: ");
    Serial.print(*time2);
    Serial.print("\t\tdelay time: ");
    Serial.println(delayTime);
  //check for overflow
  intOverflow(time1, time2);
  //check the time delay 
  if((*time2 - *time1) > delayTime)
  {
    return false;
  } 
  else 
  {
    //true for keep waiting
    return true;
  } 
}
