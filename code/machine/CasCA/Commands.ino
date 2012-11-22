/*
  Command: "dispense"
           "dispense <amount>"
  Action:  Dispenses a certain amount of quarters from the machine.
           If no amount is given, the minimum number of quarters
           is given (two quarters for Version 1).
*/
void dispense(int amount) {
  //TODO: Trigger the dispense pin for a short period of time
  //TODO: Repeat for number of quarters desired
}

/*
  Command: "check tube <number>"
  Action:  Returns the number of quarters currently in
           tube <number>. If there are more quarters than the
           sensor can count, '999' will be returned.
*/
int checkTube(int number) {
  //TODO: Check for valid tube number
  //TODO: Return the number of quarters in the tube
}
  
