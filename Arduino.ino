/*#include <Stepper.h>
int adim = 2038; //90 Derecelik adım sayısı
//Devir başına adım sayısı (360 derecelik tam tur için adım sayısı = 2048)
Stepper stepmotor(adim, 8, 9, 10, 11);

void setup()
{
  stepmotor.setSpeed(1000);
}

void loop()
{
  stepmotor.step(adim);
  delay(1);
  stepmotor.step(-adim);
  delay(1);
}*/

#include <Stepper.h>

// Defines the number of steps per rotation
const int stepsPerRevolution = 2038;

// Creates an instance of stepper class
// Pins entered in sequence IN1-IN3-IN2-IN4 for proper step sequence
Stepper myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11);


void setup() {
  Serial.begin(9600);  // Nothing to do (Stepper Library sets pins as outputs)
}

void loop() {

  if(Serial.available())

  {
  char data = Serial.read();
  if(data == '1')
     {myStepper.setSpeed(15);
    myStepper.step(stepsPerRevolution);
    }    
     
 }
}



/*void loop() {

  if(Serial.available())

  {
  char data = Serial.read();
  if(data == '1')
     {myStepper.setSpeed(5);
    myStepper.step(stepsPerRevolution);}
  else {
   if(data == '0')  
     myStepper.setSpeed(15);
  myStepper.step(-stepsPerRevolution); 
      }
  }}
 */



 
  /*// Rotate CW slowly at 5 RPM
  myStepper.setSpeed(5);
  myStepper.step(stepsPerRevolution);
  delay(1000);
  
  // Rotate CCW quickly at 10 RPM
  myStepper.setSpeed(15);
  myStepper.step(-stepsPerRevolution);
  delay(1000);
*/
