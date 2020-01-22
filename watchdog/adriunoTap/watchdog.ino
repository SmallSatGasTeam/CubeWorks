//this is the adruino watchdog code it is still in the prototyping phase as such it will be build to run on the adruino uno.
//include the watch dog libray. 
# include <avr/wdt.h>

//the  button
const int button = 13;
//LED pin
const int LED = 8;

//the button read varible
int buttonState = 0;

void setup() 
{
  //this code will set the watch dog to the desinated time,in this case 4 seconds. 
  wdt_enable(WDTO_4S);
  //this sets the button and led pins up
  pinMode(LED, OUTPUT);
  pinMode(button, INPUT);
  //this code is for testing
  Serial.begin(9600);
  Serial.println("Starting>>>");
  digitalWrite(LED, HIGH);
  delay(1000);
  digitalWrite(LED, LOW);
}

void loop() 
{
  //this code rest the watchdog
  wdt_reset();
    //this code runs so that we can see the board is working
    //read the button
    buttonState = digitalRead(button);
    Serial.println(buttonState);
    while(buttonState == digitalRead(button)){}
    //this if state ment will break the loop so that the wd will rest.
     if(buttonState == HIGH)
    {
      Serial.println("break the loop, the pi works");
      delay(500);
    }
  //if this line prints the adruino has recive an input
  Serial.println("resume the void loop");
  buttonState = digitalRead(button);
  Serial.println(buttonState);
}
