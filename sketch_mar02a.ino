#include "MeOrion.h"
#include <SoftwareSerial.h>
#include <Wire.h>

MeUltrasonicSensor ultraSensor3(PORT_4);
Me7SegmentDisplay sevseg4(PORT_3);
MeSoundSensor soundSensor(PORT_8);
MeJoystick joystick(PORT_7);
//MeBluetooth bluetooth(PORT_5);
int reps;
int set;
int seconds;
int seconder;

int smallestTime = 50;//50 milli
int repCDR = 1000 / smallestTime;// 1 seconds
int repCoolDown = repCDR;
int setCDR = 1000 / smallestTime * 3;//3 secs
int setCoolDown = setCDR; 
double soundLevel;

int x = 0;
int y = 0;
void setup() {
  Serial.begin(115200);
  //bluetooth.begin(115200);
  sevseg4.display(999);
  delay(1000);
  sevseg4.display(0);
  //Serial.println("Bluetooth Start!");
}

void loop() {
  soundLevel = soundSensor.strength();
//  seconder++;
  x = joystick.readX();
  y = joystick.readY();
//  Serial.print("Joystick X = ");
//  Serial.print(x);
//  Serial.print("Joystick Y = ");
//  Serial.print(y);
//  if (x > 400 && setCoolDown == 0) {
//    Serial.print("Reps: ");
//    Serial.print(reps);
//    Serial.print("\n");
//    setCoolDown = setCDR;
//  }
  if (x < -400 && setCoolDown == 0) {
    set++;
    reps = 0;
    Serial.print(reps);
    setCoolDown = setCDR;
  }
  if (soundLevel > 300 && repCoolDown == 0) {
    reps++;
    repCoolDown = repCDR;
  }
  if (repCoolDown > 0) {
    repCoolDown--;
  }
  if (setCoolDown > 0) {
    setCoolDown--;
  }
  sevseg4.display(reps);
//  Serial.println(reps);
//  if (Serial.available()) {
//    bluetooth.write(Serial.read());
//  }
  delay(smallestTime);
}
