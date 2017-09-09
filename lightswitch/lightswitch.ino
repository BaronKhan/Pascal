#include <RCSwitch.h>
#include <Servo.h>

#define DEBUG 0

//RF signals
//off = 1367
//on = 2728

RCSwitch mySwitch;
Servo offServo;
Servo onServo;

void switchOff();
void switchOn();

void setup()
{
  Serial.begin(9600);
  mySwitch.enableReceive(0);  //Receiver on interrupt 0 => that is pin #2
  offServo.attach(9);
  onServo.attach(10);
}

bool doSwitch = true;

void loop()
{
offServo.write(25);
onServo.write(105);
  
#if DEBUG
    if (doSwitch) {
      switchOn();
    }
    else {
      switchOff();
    }
    delay(2000);
    doSwitch = !doSwitch;
#else
  if (mySwitch.available())
  {
    int value = mySwitch.getReceivedValue();

    if (value == 2728) {
      Serial.println("Received on signal");
      switchOn();
      delay(15); 
    }
    else if (value == 1367) {
      Serial.println("Received off signal");
      switchOff();
      delay(15); 
    }

    mySwitch.resetAvailable();
  }
#endif
}

void switchOff()
{
  offServo.write(105);
  delay(2000);
  offServo.write(25);
}
void switchOn()
{
  onServo.write(25);
  delay(2000);
  onServo.write(105);
}

