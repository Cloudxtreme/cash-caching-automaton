/*
  Command: "dispense"
           "dispense <amount>"
  Action:  Dispenses a certain amount of quarters from the machine.
           If no amount is given, the minimum number of quarters
           is given (two quarters for Version 1).
*/
void dispense(int amount) {
  // Check to see if enough coins are in the machine:
  if (getCoinsLeft() >= amount)
  {
    // Dispense "amount" number of times:
    for (int i=0; i<amount; i++)
    {
      // Trigger the relay to dispense once:
      digitalWrite(RELAY_DISP_PIN, LOW);
      delay(250);
      // Release the relay:
      digitalWrite(RELAY_DISP_PIN, HIGH);
      delay(250);
      // Decrease number of coins remaining:
      coinsDispensed();
    }
  }
  else
  {
    Serial.println("Insufficient coins in machine.");
  }
}

/*
  Command: "check tube <number>"
  Action:  Returns the number of quarters currently in
           tube <number>. If there are more quarters than the
           sensor can count, '999' will be returned.
*/
void checkTube(int number) {
  Serial.print(getCoinsLeft());
  Serial.println(" coins remaining.");
  //TODO: Check for valid tube number
  //TODO: Return the number of quarters in the tube
}

/*
  Command: "refill"
  Action:  Sets the number of coins in machine to FULL_AMOUNT. 
*/
void refill() {
  refillCoins();
}
  
