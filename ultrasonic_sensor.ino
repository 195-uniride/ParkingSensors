#define trigPin 10
#define echoPin 13
#include <SPI.h>
#include <SD.h>
File myFile;
float previousD;
int i;
void setup() {
  Serial.begin (9600);
  previousD = 0;
  i = 0;
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  float duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
 
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) * 0.0344;

  if(i==4){
    float diff = abs(distance - previousD);
    
    if (distance >= 400 || distance <= 2){
    //Serial.print("Distance = ");
    //Serial.println("Out of range");
    }
    else if (previousD != distance && diff>=2.00){
      Serial.println(distance);
      delay(500);
    }
    i=0;
    
  }
  delay(150);

  if(i==0 && distance < 300){
    previousD = distance;
  }
  i = i+1;
}
