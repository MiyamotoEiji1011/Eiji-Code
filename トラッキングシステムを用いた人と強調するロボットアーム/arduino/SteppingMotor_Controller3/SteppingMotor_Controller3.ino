#include <TimerOne.h>

#define MotorA1 8
#define MotorA2 9

#define MotorB1 5
#define MotorB2 6

int motorInterval1 = 80;
int motorInterval2 = 80;

const int sensor1 = 13;
const int sensor2 = 12;


void setup() {

  Serial.begin(115200);

  pinMode(MotorA1, OUTPUT);
  pinMode(MotorA2, OUTPUT);
  
  pinMode(MotorB1, OUTPUT);
  pinMode(MotorB2, OUTPUT);

  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);

  Timer1.initialize(5);
  Timer1.attachInterrupt(init_motor);
}

void init_motor () {
  //Motor A ------//
  static int motorTime1;

  if (motorInterval1 >= 0)digitalWrite(MotorA1, LOW);
  if (motorInterval1 < 0)digitalWrite(MotorA1, HIGH);

  motorTime1 ++;
  if (motorTime1 > abs(motorInterval1)) {
    motorTime1 = 0;
  }
  if (motorTime1 == 0)digitalWrite(MotorA2, HIGH);
  if (motorTime1 == 1)digitalWrite(MotorA2, LOW);

  //Motor B ------//
  static int motorTime2;

  if (motorInterval2 >= 0)digitalWrite(MotorB1, LOW);
  if (motorInterval2 < 0)digitalWrite(MotorB1, HIGH);

  motorTime2 ++;
  if (motorTime2 > abs(motorInterval2)) {
    motorTime2 = 0;
  }
  if (motorTime2 == 0)digitalWrite(MotorB2, HIGH);
  if (motorTime2 == 1)digitalWrite(MotorB2, LOW);
}

void loop() {
  bool date1 = digitalRead(sensor1);
  bool date2 = digitalRead(sensor2);

  if(date1){
    motorInterval1 = 0;
  }

  if(date2){
    motorInterval2 = 0;
  }

  Serial.print("date1:");Serial.print(date1);
  Serial.print(" / ");
  Serial.print("motorInterval1:");Serial.print(motorInterval1);
  Serial.print(" / ");
  Serial.print("date2:");Serial.print(date2);
  Serial.print(" / ");
  Serial.print("motorInterval2:");Serial.print(motorInterval2);
  Serial.println();
}
