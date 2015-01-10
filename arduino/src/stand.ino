const int ECHO = 7;
const int TRIGGER = 8;

void setup() {
  Serial.begin(9600);

  pinMode(ECHO, INPUT);
  pinMode(TRIGGER, OUTPUT);
}

/*
 * code for reading the ultrasonic sensor based on:
 * http://arduinobasics.blogspot.com/2012/11/arduinobasics-hc-sr04-ultrasonic-sensor.html
 */
int readDistanceInCm() {
  digitalWrite(TRIGGER, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIGGER, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIGGER, LOW);
  int duration = pulseIn(ECHO, HIGH);

  // not sure what 58.2 is - the article above indicates the distance
  // calculated is in cm based on the speed of sound
  int distance = duration / 58.2;

  return distance;
}

void checkStatus() {
  int distance = readDistanceInCm();

  if(distance < 0)
    return;

  Serial.print("{\"distance_cm\": ");
  Serial.print(distance);
  Serial.println("}");
}

void loop() {
  checkStatus();
  delay(1000);
}
