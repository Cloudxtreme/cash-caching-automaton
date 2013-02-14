// Blinks the light N times in N seconds, indicating that the 
//  machine is low on funds after a withdrawal. 
void blinkLightNumberOfTimes(int numberOfTimes) {
  for(int i = 0; i < numberOfTimes; ++i) {
    digitalWrite(RELAY_LIGHT_PIN, LOW);
    delay(500);
    digitalWrite(RELAY_LIGHT_PIN, HIGH);
    delay(500);
  }
}
// Turns the light on indefinitely, indicating that the machine is
//  empty.
void turnOnLight() {
  digitalWrite(RELAY_LIGHT_PIN, LOW);
}
// Turns the light off indefinitely, indicating that the machine
//  status is normal.
void turnOffLight() {
  digitalWrite(RELAY_LIGHT_PIN, HIGH);
}
