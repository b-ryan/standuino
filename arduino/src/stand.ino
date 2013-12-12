const int RED = 2;
const int GREEN = 4;
const int ECHO = 7;
const int TRIGGER = 8;

const int DISTANCE_THRESHOLD_CM = 135;

boolean _standing = false;
boolean _initialized = false;

void setStanding(boolean standing) {
  _standing = standing;

  int gVal = _standing ? HIGH : LOW; // value of the green pin
  digitalWrite(GREEN, gVal);
  digitalWrite(RED, (gVal + 1) % 2);

  Serial.print("event: ");
  Serial.println(_standing ? "standing" : "sitting");
}

void setup() {
  Serial.begin(9600);

  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(TRIGGER, OUTPUT);
}

/*
 * code for reading the ultrasonic sensor based on:
 * http://arduinobasics.blogspot.com/2012/11/arduinobasics-hc-sr04-ultrasonic-sensor.html
 */
int readSensor() {
  digitalWrite(TRIGGER, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIGGER, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIGGER, LOW);
  int duration = pulseIn(ECHO, HIGH);

  int distance = duration / 58.2;

  return distance;
}

void checkStatus() {
  int distance = readSensor();

  if(distance < 0)
    return;

  Serial.print("distance: ");
  Serial.println(distance);

  boolean standing = distance < DISTANCE_THRESHOLD_CM;
  if(!_initialized || _standing != standing) {
    setStanding(standing);
    _initialized = true;
  }
}

void loop() {
  checkStatus();
  delay(1000);
}
