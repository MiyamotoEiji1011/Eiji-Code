#include<Servo.h>
Servo servo;

// センサ
const int sensor1 = 5;
const int sensor2 = 6;

#define sensor3 A0

//出力信号
#define sendA1 7
#define sendA2 8
#define sendB1 9
#define sendB2 10
#define sendC1 11
#define sendC2 12
#define ENA 13

const int connect_pin = 0;  // 接続確認LED

bool serial_connect = false;

void setup() {
  Serial.begin(115200);

  servo.attach(3);

  //センサ
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);

  pinMode(sendA1, OUTPUT);
  pinMode(sendA2, OUTPUT);
  pinMode(sendB1, OUTPUT);
  pinMode(sendB2, OUTPUT);
  pinMode(sendC1, OUTPUT);
  pinMode(sendC2, OUTPUT);
  pinMode(ENA, OUTPUT);

  pinMode(connect_pin, OUTPUT);
}


void loop() {
  // 同期処理
  while (!serial_connect) {

    Serial.println("don't connecting...");

    if (Serial.available() > 0) {
      String data = Serial.readStringUntil('\n');
      data.trim();
      digitalWrite(connect_pin, LOW);

      if (data == "serial_connecting") {
        Serial.println("serial_connected");
        digitalWrite(connect_pin, HIGH);
        serial_connect = true;

        Serial.println("Main process start");
        break;
      }
    }
  }

  // メイン処理 //
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();

    if (data == "motor_offset") {
      Serial.println("processing_now");
      motor_offset();
      Serial.println("processing_completed");
    }

    if (data == "motorA_start") {
      Serial.println("processing_now");
      motorA_set();
      Serial.println("processing_completed");
    }

    if (data == "motorB_start") {
      Serial.println("processing_now");
      motorB_set();
      Serial.println("processing_completed");
    }

    if (data == "servo_start") {
      Serial.println("processing_now");
      servo_set();
      Serial.println("processing_completed");
    }

    //終了コマンド
    if (data == "process_end") {
      delay(10);
      Serial.println("end_return");
      while (true) {
        delay(1000);
      }
    }
  }

}

void servo_set() {
  servo.write(100);
  delay(100);
  while (1) {
    int data;
    for (int i = 0; i < 10; i++) {
      data = data + analogRead(sensor3);
    }
    data = data / 10;

    if (data < 20) {
      servo.write(125);
      break;
    }

  }
}

void motorAB_set() {
  digitalWrite(sendA1, HIGH);
  digitalWrite(sendA2, HIGH);

  digitalWrite(sendB1, HIGH);
  digitalWrite(sendB2, HIGH);
  bool flagA, flagB;

  while (true) {
    if (Serial.available() > 0) {
      String data = Serial.readStringUntil('\n');
      data.trim();

      if (data == "motorA_stop") {
        digitalWrite(sendA1, LOW);
        digitalWrite(sendA2, LOW);
        Serial.println("stop_motorA");
        flagA = true;
      }
      if (data == "motorB_stop") {
        digitalWrite(sendB1, LOW);
        digitalWrite(sendB2, LOW);
        Serial.println("stop_motorB");
        flagB = true;
      }
      if (flagA && flagB) {
        break;
      }
    }
  }
  delay(10);
}

void motorA_set() {
  digitalWrite(sendA1, HIGH);
  digitalWrite(sendA2, HIGH);
  while (true) {
    if (Serial.available() > 0) {
      String data = Serial.readStringUntil('\n');
      data.trim();

      if (data == "motorA_stop") {
        digitalWrite(sendA1, LOW);
        digitalWrite(sendA2, LOW);
        Serial.println("stop_motorA");
        break;
      }
    }
  }
  delay(10);
}

void motorB_set() {
  digitalWrite(sendB1, HIGH);
  digitalWrite(sendB2, HIGH);
  while (true) {
    if (Serial.available() > 0) {
      String data = Serial.readStringUntil('\n');
      data.trim();

      if (data == "motorB_stop") {
        digitalWrite(sendB1, LOW);
        digitalWrite(sendB2, LOW);
        Serial.println("stop_motorB");
        break;
      }
    }
  }
  delay(10);
}



void motor_offset() {
  digitalWrite(sendA1, HIGH);
  digitalWrite(sendA2, LOW);
  digitalWrite(sendB1, HIGH);
  digitalWrite(sendB2, LOW);

  while (true) {
    bool date1 = digitalRead(sensor1);
    bool date2 = digitalRead(sensor2);
    Serial.print(date1); Serial.println(date2);

    if (date1) {
      digitalWrite(sendA1, LOW);
      digitalWrite(sendA2, LOW);
    }
    if (date2) {
      digitalWrite(sendB1, LOW);
      digitalWrite(sendB2, LOW);
    }
    if (date1 && date2) {
      break;
    }
  }
  delay(10);
}
