const int connect_pin = 0;  // 接続確認LED

bool serial_connect = false;

void setup() {
  Serial.begin(115200);
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

      if (data == "Serial connecting...") {
        Serial.println("Serial connected");
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

    if (data == "step_motor offset") {
      Serial.println("...");
      //stepmotor
      Serial.println("Processing completed");
    }
  }

  
}
