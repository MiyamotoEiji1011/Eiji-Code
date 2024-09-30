#include <A4988.h>

const int MOTOR_STEPS = 1600;

const int A_DIR  =  8;
const int A_STEP =  9;

const int B_DIR  =  5;
const int B_STEP =  6;

float rpm      = 60;
int microsteps = 30;

A4988 A_stepper(MOTOR_STEPS, A_DIR, A_STEP);
A4988 B_stepper(MOTOR_STEPS, B_DIR, B_STEP);

const int A_ir = 10;
const int B_ir = 4;

void setup() {
  Serial.begin(9600);
  A_stepper.begin(rpm, microsteps);
  B_stepper.begin(rpm, microsteps);

  pinMode(A_ir, INPUT);
  pinMode(B_ir, INPUT);
}

void loop() {
  if (digitalRead(A_ir) == 1) {
    Serial.println("A-Motor stoped");

    Serial.println("A-Motor right");
    A_stepper.rotate(600);

    Serial.println("A-Motor left");
  }
  A_stepper.rotate(-10);

  if (digitalRead(B_ir) == 1) {
    Serial.println("B-Motor stoped");

    Serial.println("B-Motor right");
    B_stepper.rotate(600);

    Serial.println("B-Motor left");
  }
  B_stepper.rotate(-10);
}
