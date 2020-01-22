//this is the adruino watchdog code it is still in the prototyping phase as such it will be build to run on the adruino uno.
//This is the second prototype, this code includes a second timer, which will run off the inter clock of the Adriuno 
//include the watch dog libray. 
//
//sudo code
//
//turn on(pi, and watchdog)
//wait for pi input
//if pi delays more then 4 seconds rest
//else rest watchdog
//repet void loop

# include <avr/wdt.h>

//the  button
const int button = 13;
//LED pin
const int LED = 8;
//The pi delay const
const int PI_CHECK = 4000;

//the button read varible
int buttonState = 0;

void setup() 
{
  //this code will set the watch dog to the desinated time,in this case 4 seconds. 
  wdt_enable(WDTO_8S);
  //this sets the button and led pins up
  pinMode(LED, OUTPUT);
  pinMode(button, INPUT_PULLUP);
  //this code is for testing
  Serial.begin(9600);
  Serial.println("Starting>>>");
  //simulate turning the pi on
  digitalWrite(LED, HIGH);
  delay(1000);
  digitalWrite(LED, LOW);
}

void loop() 
{
  //this code rest the watchdog
  wdt_reset();
  
  //set timer 
  long timer = millis();

  //set the tiem_check bool to true
  bool time_check = true;

  //set the watchdog bool to false, if it remains un changed it will reset the pi
  bool W_D_PI = false;
  
  //this code runs so that we can see the board is working
  //read the button
  buttonState = digitalRead(button);
  
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
    buttonState = digitalRead(button);
    delay(50);//This line of code is ONLY for the prototype, it is a delay built to debounce that button and will not apply to the pi.
   }
  }

  Serial.println("While loop broken");
  //this logic desides if we are going to reset the pi if W_D_PI = false we reset, if it equals true we pass it over and reset the loop.
  if(W_D_PI == false)
  {
    //reset pi
    //this sumilates the pi resteting
    digitalWrite(LED, HIGH);
    delay(100);
    digitalWrite(LED, LOW);
    delay(100);
    digitalWrite(LED, HIGH);
    delay(100);
    digitalWrite(LED, LOW);
  }
}
