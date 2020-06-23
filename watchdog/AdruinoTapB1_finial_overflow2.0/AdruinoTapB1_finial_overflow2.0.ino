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

//the  button
#define BUTTON 11
//MOSFIT pin, make sure not to use the #define function here. The #define actually repalces code in 
//beetle and this will cause the digital pin not to initialize incorrectly. 
const int MOSFIT = 10;
//This is the delay for the pi to boot up. It will get a little more the 5 seconds. (BOOT_DEALY + PI_CHECK)
const int BOOT_DELAY = 1000;
//The pi delay const
#define PI_CHECK 4000
//set LED to high
const int LED = 13;

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


}

void loop() 
{  
  //This is where you want to enable the watchdog, just be careful not to set the frequency too low. 
  //If it does get set too low you will have to hold the pins and then upload a new sketch. This will
  //take several tries as it is a timing game. 
  //Note: The wdt_enable does reset the watchdog timer. 
  wdt_enable(WDTO_8S);

  //call the watchdog protocol, this is taken from the adruinoTap2 code.
  bool Reset = watchdogProtocol();

  //call the turn fuction
  turn(Reset);
  

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
  
  //if the PI state is HIGH then it has sent the heartbeat and we reset the count, if not we continue adding to time_actual until we exceed 4,000 in which case the pi will be reset. 
  while(time_check == true)
  {
    //set this to false to start with the default is a reboot is needed
    bool W_D_PI = false;
    //get time actual
    long time_actual = millis();

    //check for int overflow 
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
   //if the state goes form LOW to HIGH we break the loop
   if(buttonState == HIGH)
   {
//    while(buttonState == digitalRead(BUTTON)){};
    //set the pi watch dog to true, meaning no rest is needed
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
void turn(bool check)
{
  if(check == false)
  {
    //reset pi
    //pi off
    digitalWrite(MOSFIT, HIGH);
    delay(5000);
    //pi on
    digitalWrite(MOSFIT, LOW);
    //delay to give the pi time to boot, it will have a max of 5 seconds to boot
    delay(BOOT_DELAY);
  }
}


//this method quick for int overflow to make sure that the clock does not exceed the long int limit
void intOverflow(long *time1, long *time2)
{
  //check for over flow
  if (*time1 > *time2)
  {
    //if so delay one second and reset the times
    delay(1000);
    *time1 = millis();
    *time2 = millis();
  }
}

//this method is to check and see if we have received any communication over UART and then calls the OFF func
///////////////////////////TODO/////////////////////////////////////////

//this method turns the pi off
void OFF(void)
{
  digitalWrite(MOSFIT, HIGH);
}
