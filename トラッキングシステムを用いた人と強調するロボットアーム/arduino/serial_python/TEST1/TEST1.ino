const int connect_pin = 13;  // 接続確認LED
#define sendA 10

bool serial_connect = false;

void setup() {
  Serial.begin(115200);
  
  pinMode(connect_pin, OUTPUT);
  pinMode(sendA, OUTPUT);
  
  digitalWrite(connect_pin, LOW);
  
}

void loop() {
  // 同期処理
  while (!serial_connect) {
    Serial.println("don't connecting...");

    if (Serial.available() > 0) {
      String data = Serial.readStringUntil('\n');
      data.trim();
      digitalWrite(connect_pin, LOW);

      if (data == "serial_connect") {
        digitalWrite(connect_pin, HIGH);
        
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

    if (data == "led_start") {
      Serial.println("...");
      digitalWrite(sendA, HIGH);
      Serial.println("processing_completed");
    }

    if (data == "led_stop") {
      Serial.println("...");
      digitalWrite(sendA, LOW);
      Serial.println("processing_completed");
    }
  }


}
