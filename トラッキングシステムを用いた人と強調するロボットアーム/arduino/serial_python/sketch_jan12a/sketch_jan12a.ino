byte data = 0;

void setup(){
  Serial.begin(115200);
  
  pinMode(22, OUTPUT);
  digitalWrite(22, LOW);
}

void loop(){
  if (Serial.available() > 0){
    data = (byte)Serial.read();
    
    if(data == 123){
      digitalWrite(22, HIGH);
      delay(3000);
    }
    else{
      digitalWrite(22, LOW);
    }    
  }
}
