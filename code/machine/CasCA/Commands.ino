/*
  Command: "dispense"
           "dispense <amount>"
  Action:  Dispenses a certain amount of quarters from the machine.
           If no amount is given, the minimum number of quarters
           is given (two quarters for Version 1).
*/
void dispense(int amount) {
  // Dispense "amount" number of times:
  for (int i=0; i<amount; i++) {
    // Trigger the relay to dispense once:
    digitalWrite(RELAY_DISP_PIN, LOW);
    delay(250);
    // Release the relay:
    digitalWrite(RELAY_DISP_PIN, HIGH);
    delay(250);
  }
}

/*
  Command: "light blink"
           "light blink <amount>"
  Action:  Blinks the machine's light a certain number of times.
           If no amount is given, the light will blink three times.
*/
void blinkLightNumberOfTimes(int numberOfTimes) {
  for(int i = 0; i < numberOfTimes; ++i) {
    digitalWrite(RELAY_LIGHT_PIN, LOW);
    delay(500);
    digitalWrite(RELAY_LIGHT_PIN, HIGH);
    delay(500);
  }
}
void blinkLightNumberOfTimes() {
  //If no amount is given, blink three times:
  blinkLightNumberOfTimes(3);
}

/*
  Command: "light on"
  Action:  Turns the light on indefinitely, usually indicating that
           the machine is empty.
*/
void turnOnLight() {
  digitalWrite(RELAY_LIGHT_PIN, LOW);
}

/*
  Command: "light off"
  Action:  Turns the light off indefinitely, usually indicating that
           the machine is operational and not empty.
*/
void turnOffLight() {
  digitalWrite(RELAY_LIGHT_PIN, HIGH);
}

/*
  Command: "relay on"
  Action:  Turns the relay on indefinitely, controlling a light or
           other device connected to the outlet.
*/
void turnOnRelay() {
  digitalWrite(RELAY_MISC_PIN, HIGH);
}

/*
  Command: "relay off"
  Action:  Turns the relay off indefinitely, controlling a light or
           other device connected to the outlet.
*/
void turnOffRelay() {
  digitalWrite(RELAY_MISC_PIN, LOW);
}

/*
  Command: "debug on"
  Action: Enables the output of debug messages over the serial port.
*/
void enableDebug() {
  if (debugMode == true) {
    printDebug("Debug mode is already enabled.\r\n");
  }
  else {
    debugMode = true;
    printDebug("Debug output is now enabled.\r\n");
  }
}

/*
  Command: "debug off"
  Action: Disables the output of debug messages over the serial port.
*/
void disableDebug() {
  printDebug("Debug mode is now disabled.");
  debugMode = false;
}

/*
  Command: "temperature"
  Action: Returns the current temperature of the vending machine in
          degrees Celsius (°C).
*/
float getTemperature() {
  return(runTempControl());
}
