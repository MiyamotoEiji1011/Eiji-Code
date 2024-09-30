#include "MPU6050.h"
MPU6050 accelgyro;
#include <MadgwickAHRS.h>
Madgwick MadgwickFilter;

int16_t ax, ay, az;
int16_t gx, gy, gz;
float ROLL, PITCH, YAW;

const int INA1 = 6;
const int INA2 = 11;

const int INB1 = 10;
const int INB2 = 9;

const float Kp = 142.0;
const float Ki = 20.0;
const float Kd = 10.0;
const float Target = 0;

float P, I, D;
float dt, pretime,preP;

void setup() {
  Wire.begin();
  Serial.begin(115200);
  accelgyro.initialize();
  delay(300);
  MadgwickFilter.begin(100);

  Motor(0);
}

void loop() {
  accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  MadgwickFilter.updateIMU(gx / 131.0, gy / 131.0, gz / 131.0, ax / 16384.0, ay / 16384.0, az / 16384.0);
  PITCH = MadgwickFilter.getPitch();

  dt = (micros() - pretime) / 1000000;
  pretime = micros();

  P = (Target - PITCH);
  I += P*dt;
  D = (P - preP) / dt;
  preP = P;

  if (100 < abs(I * Ki)) {
    I = 0;
  }
  
  float M = Kp * P + Ki * I + Kd * D;
  
  Motor(M);
}

void Motor(float i) {
  if (i == 0) {
    analogWrite(INA1, LOW);
    analogWrite(INA2, LOW);
    analogWrite(INB1, LOW);
    analogWrite(INB2, LOW);
  }
  if (i > 0) {
    analogWrite(INA1, abs(i));
    analogWrite(INA2, 0);
    analogWrite(INB1, 0);
    analogWrite(INB2, abs(i));
  }
  if (i < 0) {
    analogWrite(INA1, 0);
    analogWrite(INA2, abs(i));
    analogWrite(INB1, abs(i));
    analogWrite(INB2, 0);
  }
}
