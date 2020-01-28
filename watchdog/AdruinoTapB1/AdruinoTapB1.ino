//This is the protype code for the adruinoTap protocal, but built inparticular for the beetle. 
//It uses the same concepts as the adriunoTap2, however the adruino beetle doesn't work well with
//the watchdog proticol. To be spesific, the watchdog doesnt work well with the beetle's boot 
//loader. It will cause an infinte loop. The best way around this is to disable the watchdog
//for the void setup function and then use it with in the void loop. This is the main diffrence 
//between the adruinoTap2 and this program the adriunoTap3. 
//
//Note: This will be the first implitation of the beetle.
//NOte: This will be the first implitation of an MOSFIT.
//
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
//Compile instructions: Plug in the beetle in to your computer, on windows you will see
//a message whitch will tell you "setting your beetle". The open the adruino ide. Go to 
//tools and select the aduino Leonardo under the board tab. Make sure you check the port
//is set to the board. Upload the sketch. (It may take afew tries.)
//
//Note: It is very possible that the beetle will not come up on your port. Try unpluging it
//then try resting the board, then try resting your computer. If none of that works, try holding
//the rest button and then uploading the code and relasing the reset button
//
//Note: Each beetle has a unique reset button so make sure to look it up online! If you hold the
//wrong pins you can end your board. RIP


//include the wd proticol
#include<avr/wdt.h>

//the  button
#define BUTTON 11
//MOSFIT pin
#define MOSFIT 13
//The pi delay const
#define PI_CHECK 4000

void setup() 
{
 //IMPORTANT NOTE: Make sure watchdog is disabled for this part of the code, if not the code
 //will compile and run. However after the watchdog resests for the first time the beetle 
 //will no longer run. The beetle will get cought in an infinite loop. At that point you 
 //need to hold the rest pins up load the sketch and then relase the reset pins. You have 
 //to manulaly break the loop. 
 wdt_disable();

 //set up the pins
 pinMode(MOSFIT, OUTPUT);
 pinMode(BUTTON, INPUT_PULLUP);

 //Star the serial monitor. I haven't been able to look into the serial moniter much however
 //it might help if we run the beelte on a lower serial input. 
 Serial.begin(9600);

 Serial.println("Starting>>>");
 //simulate turning the pi on
 digitalWrite(MOSFIT, LOW);
 delay(1000);
 digitalWrite(MOSFIT, HIGH);
 delay(500);
 digitalWrite(MOSFIT, LOW);
}

void loop() 
{
  //This is where you want to enable the watchdog, just be careful not to set the frequency too low. 
  //If it dose get set too low you will have to hold the pins and then up load a new sketch. This will
  //take servel trys as it is a timing game. 
  wdt_enable(WDTO_8S);

  //call the watchdogProtocol, this is taken form the adruinoTap2 code.
  bool Reset = watchdogProtocol();

  //call the turn fuction
  turn(Reset);
  

}

bool watchdogProtocol()
{ //set timer 
  long timer = millis();

  //set the tiem_check bool to true
  bool time_check = true;

  //set the watchdog bool to false, if it remains un changed it will reset the pi
  bool W_D_PI = false;
  
  //this code runs so that we can see the board is working
  //read the button
  int buttonState = digitalRead(BUTTON);
  
  //Serial.println(buttonState);//use this code to see the button state if that become relavent. (del the first //)
  
  delay(50);//This line of code is ONLY for the prototype, it is a delay built to debounce that button and will not apply to the pi.

  //record the time that we start the loop
  long time_actual = millis();
  
  //if the button state is LOW then it has been pressed and we state the loop over again, if not we countinue adding to time_actual until we exsed 4,000 in witch case the pi will be reset. 
  while(time_check == true)
  {
    //get time actual
    long time_actual = millis();
   
    //this logic test is the timer 
    if(PI_CHECK > time_actual - timer)
    {
     Serial.println("Waiting");
     time_check = true;
    }
    else
    {
      Serial.println("End loop");
      time_check = false;
    }
   

   //check to see if in what condition the button is in
   //if it is LOW we break the loop
   if(buttonState == LOW)
   {
    while(buttonState == digitalRead(BUTTON)){};
    //set the pi watch dog to true
    W_D_PI = true;
    //break the while loop
    time_check = false;
   } 
   else
   {
    Serial.println(PI_CHECK - (time_actual - timer));
    Serial.println("No pi input");
    //read the button
    buttonState = digitalRead(BUTTON);
    delay(50);//This line of code is ONLY for the prototype, it is a delay built to debounce that button and will not apply to the pi.
   }
  }
  return W_D_PI;
}

void turn(bool check)
{
  if(check == false)
  {
    //reset pi
    //this sumilates the pi resteting
    digitalWrite(MOSFIT, HIGH);
    delay(1000);
    digitalWrite(MOSFIT, LOW);
    delay(1000);
    digitalWrite(MOSFIT, HIGH);
    delay(1000);
    digitalWrite(MOSFIT, LOW);
    delay(1000);
    digitalWrite(MOSFIT, HIGH);
  }
}
