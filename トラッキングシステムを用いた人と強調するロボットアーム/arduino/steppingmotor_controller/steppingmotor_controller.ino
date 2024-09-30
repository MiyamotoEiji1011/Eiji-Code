int step_pin = 13;
int dir_pin = 12;
int relay_pin = 11;

#include <A4988.h>

const int MOTOR_STEPS = 1600;
const int DIR  =  8;
const int STEP =  9;

float rpm      = 30;
int microsteps = 30;

A4988 stepper(MOTOR_STEPS, dir_pin, step_pin);

void setup() {
  stepper.begin(rpm, microsteps);
  digitalWrite(relay_pin, LOW);

  pinMode(9, INPUT);
}

void loop() {
  while (!digitalRead(9)) {
    stepper.rotate(-1);
    delay(1);
  }

  stepper.rotate(360*2);
  delay(1000);
}
