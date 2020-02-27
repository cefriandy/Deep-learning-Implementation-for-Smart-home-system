#include <SoftwareSerial.h>

//Define the pins used for receiving
//and transmitting information via Bluetooth
const int rxpin = 0;
const int txpin = 1;

#include <Servo.h>
Servo servo;
SoftwareSerial bluetooth(rxpin, txpin);

char value1 ;
void setup()
{
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(11, OUTPUT);
  servo.attach(8);
  servo.write(0);
  Serial.begin(9600);
  bluetooth.begin(9600);
  bluetooth.println("Bluetooth ready");
}

void loop()
{
  while (bluetooth.available() >0)
  {
    value1 = bluetooth.read();
  }

    if (value1 == 'h') {
      digitalWrite(13, HIGH);
      servo.write(90);
      delay(100);
      Serial.println("serial read: ");
      Serial.print(value1);
        for (int i = 10; i > 0; i--){
          Serial.println("go inside!!, hurry up !!");
          delay(1000);
        }
        servo.write(0);
      Serial.println("door is closed");
      delay(1000);
     }
     
  
    if (value1 == 'a') {
      digitalWrite(12, HIGH);
      servo.write(90);
      delay(100);
      Serial.println("serial read: ");
      Serial.print(value1);
      for (int i = 10; i > 0; i--){
          Serial.println("go inside!!, hurry up !!");
          delay(1000);
        }
        servo.write(0);
      Serial.println("door is closed");
      delay(1000);  
      }
  
    if (value1 == 's') {
      digitalWrite(11, HIGH);
      servo.write(90);
      delay(100);
      Serial.println("serial read: ");
      Serial.print(value1);
      for (int i = 10; i > 0; i--){
          Serial.println("go inside!!, hurry up !!");
          delay(1000);
        }
        servo.write(0);
      Serial.println("door is closed");
      delay(1000); 
      }
      value1 = "";
  }
