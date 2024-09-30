#include <TimerOne.h>

#define MotorA1 13
#define MotorA2 12
#define MotorB1 11
#define MotorB2 10
#define MotorC1 9
#define MotorC2 8
#define ENA 7

#define readA1 0
#define readA2 1
#define readB1 2
#define readB2 3
#define readC1 4
#define readC2 5
#define readENA 6

#define Vr A0

int motorInterval1, motorInterval2, motorInterval3;
bool enaA, enaB, enaC;
bool dirA, dirB, dirC;

const int connect_pin = 19;  // 接続確認LED

void setup() {
  //モーター
  pinMode(MotorA1, OUTPUT);
  pinMode(MotorA2, OUTPUT);
  pinMode(MotorB1, OUTPUT);
  pinMode(MotorB2, OUTPUT);
  pinMode(MotorC1, OUTPUT);
  pinMode(MotorC2, OUTPUT);
  pinMode(ENA, OUTPUT);

  pinMode(readA1, INPUT);
  pinMode(readA2, INPUT);
  pinMode(readB1, INPUT);
  pinMode(readB2, INPUT);
  pinMode(readC1, INPUT);
  pinMode(readC2, INPUT);
  pinMode(readENA, INPUT);

  pinMode(connect_pin, OUTPUT);

  //モータースピード0
  motorInterval1 = motorInterval2 = motorInterval3 = 4;
  enaA = enaB = enaC = false;
  dirA = dirB = dirC = false;

  for(int i=0; i<2; i++){
    digitalWrite(connect_pin, HIGH);
    delay(200);
    digitalWrite(connect_pin, LOW);
    delay(200);
  }
  digitalWrite(connect_pin, HIGH);
  delay(1000);

  Timer1.initialize(5);
  Timer1.attachInterrupt(init_motor);
  Timer1.start();
}


void loop() {
  enaA = digitalRead(readA1);
  dirA = digitalRead(readA2);

  enaB = digitalRead(readB1);
  dirB = digitalRead(readB2);

  enaC = digitalRead(readC1);
  dirC = digitalRead(readC2);

  digitalWrite(ENA, digitalRead(readENA));
}


void init_motor () {
  //Motor A ------//
  static int motorTime1;

  if(dirA)digitalWrite(MotorA2, HIGH);
  else digitalWrite(MotorA2, LOW);

  motorTime1 ++;
  if (motorTime1 > abs(motorInterval1)) {
    motorTime1 = 0;
  }
  if (enaA) {
    if (motorTime1 == 0)digitalWrite(MotorA1, HIGH);
    if (motorTime1 == 1)digitalWrite(MotorA1, LOW);
  }
  //Motor B ------//
  static int motorTime2;

  if(dirB)digitalWrite(MotorB2, HIGH);
  else digitalWrite(MotorB2, LOW);

  motorTime2 ++;
  if (motorTime2 > abs(motorInterval2)) {
    motorTime2 = 0;
  }
  if (enaB) {
    if (motorTime2 == 0)digitalWrite(MotorB1, HIGH);
    if (motorTime2 == 1)digitalWrite(MotorB1, LOW);
  }
  //Motor C ------//
  static int motorTime3;

  if(dirC)digitalWrite(MotorC2, HIGH);
  else digitalWrite(MotorC2, LOW);

  motorTime3 ++;
  if (motorTime3 > abs(motorInterval3)) {
    motorTime3 = 0;
  }
  if (enaC) {
    if (motorTime3 == 0)digitalWrite(MotorC1, HIGH);
    if (motorTime3 == 1)digitalWrite(MotorC1, LOW);
  }
}
