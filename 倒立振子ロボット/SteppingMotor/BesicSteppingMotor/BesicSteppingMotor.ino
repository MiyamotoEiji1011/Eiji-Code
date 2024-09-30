#include <Stepper.h>
#define STEPS 2048

Stepper stepper(STEPS, 8, 10, 9, 11);

void setup() {
  stepper.setSpeed(10);
}
int speed_=17;
void loop() {
  stepper.step((float)20);
  stepper.setSpeed(speed_);
  speed_--;
  if(speed_==0)speed_=17;
}
