// Arduino受信側のコード

void setup() {
  Serial.begin(115200);  // Arduinoのシリアル通信のボーレートに合わせて変更
}

void loop() {
  if (Serial.available() > 0) {
    // シリアルからデータを読み取る
    String data = Serial.readStringUntil('\n');
    
    // 改行文字を取り除く
    data.trim();
    
    // 受信したデータをスペースで分割
    int spaceIndex = data.indexOf(' ');
    if (spaceIndex != -1) {
      // データ1とデータ2を分割
      String data1_str = data.substring(0, spaceIndex);
      String data2_str = data.substring(spaceIndex + 1);
      
      // Stringからfloatへの変換
      float data1 = data1_str.toFloat();
      float data2 = data2_str.toFloat();
      
      // 受信したデータに対する処理（例：シリアルモニタに出力）
      Serial.print("Received Data: ");
      Serial.print("X = ");
      Serial.print(data1);
      Serial.print(", Y = ");
      Serial.println(data2);
    }
  }
}
