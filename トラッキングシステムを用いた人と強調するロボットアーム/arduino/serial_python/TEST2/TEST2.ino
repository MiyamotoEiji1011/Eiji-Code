#include <TimerOne.h>

// モーター
#define MotorA1 8
#define MotorA2 9

#define MotorB1 5
#define MotorB2 6

int motorInterval1, motorInterval2;

//読み込み信号
#define readA1 12
bool enaA;

const int connect_pin = 13;  // 接続確認LED

void setup() {
  //モーター
  pinMode(MotorA1, OUTPUT);
  pinMode(MotorA2, OUTPUT);

  pinMode(MotorB1, OUTPUT);
  pinMode(MotorB2, OUTPUT);

  //読み込み信号
  pinMode(readA1, INPUT);

  pinMode(connect_pin, OUTPUT);

  //モータースピード0
  motorInterval1 = analogRead(A0);

  Timer1.initialize(5);
  Timer1.attachInterrupt(init_motor);
  Timer1.start();
}

void init_motor () {
  //Motor A ------//
  static int motorTime1;

  digitalWrite(MotorA1, LOW);

  motorTime1 ++;
  if (motorTime1 > abs(motorInterval1)) {
    motorTime1 = 0;
  }
  if (enaA) {
    if (motorTime1 == 0)digitalWrite(MotorA2, HIGH);
    if (motorTime1 == 1)digitalWrite(MotorA2, LOW);
  }

}

void loop() {
  enaA = digitalRead(readA1);
  digitalWrite(connect_pin, enaA);
}
