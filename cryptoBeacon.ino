void setup() {
  pinMode(8, OUTPUT);  // LED for Buy Signal 1
  pinMode(9, OUTPUT);  // LED for Sell Signal 1
  pinMode(6, OUTPUT); //LED for Buy Signal 2
  pinMode(7, OUTPUT); //LED for Sell Signal 2
  pinMode(13, OUTPUT); //LED for Buy Signal 3
  pinMode(12, OUTPUT); //LED for Sell Signal 3
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char signal = Serial.read();
    //signal 1
    if (signal == 'B') {
      digitalWrite(8, HIGH);
      digitalWrite(9, LOW);
    } else if (signal == 'S') {
      digitalWrite(8, LOW);
      digitalWrite(9, HIGH);
    } else if (signal == 'H'){
      digitalWrite(8, HIGH);
      digitalWrite(9, HIGH);
    }
    //signal 2
    else if (signal == 'b'){
      digitalWrite(6, HIGH);
      digitalWrite(7, LOW);
    } else if (signal == 's') {
      digitalWrite(6, LOW);
      digitalWrite(7, HIGH);
    } else if (signal == 'h'){
      digitalWrite(6, HIGH);
      digitalWrite(7, HIGH);
    }
    //signal 3
    else if (signal == 'R'){
      digitalWrite(13, HIGH);
      digitalWrite(12, LOW);
    } else if (signal == 'G') {
      digitalWrite(13, LOW);
      digitalWrite(12, HIGH);
    } else if (signal == 'N'){
      digitalWrite(13, HIGH);
      digitalWrite(12, HIGH);
    }
  }
  /*test
  digitalWrite(6, HIGH);
  digitalWrite(7, HIGH);
  digitalWrite(8, HIGH);
  digitalWrite(9, HIGH);
  digitalWrite(12, HIGH);
  digitalWrite(13, HIGH);*/
}
