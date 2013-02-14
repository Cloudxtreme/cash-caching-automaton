#define FULL_AMOUNT 25 // Amount of quarters in tube to fill machine
#define SWITCH_AMOUNT 6 // Number of coins left at switch trigger

int coinsLeft = 0;

// Starts up the coin tracker by reading in the last stored coin
//  count value.
void initCoinTracker() {
  // Retrieve the last stored coint count value:
  coinsLeft = retrieveCoinCount();
}

// This funciton should be called anytime the machine is
//  refilled. It sets the coin count to the maximum count set by
//  FULL_AMOUNT.
void refillCoins() {
  coinsLeft = FULL_AMOUNT;
  storeCoinCount(coinsLeft);
}

// Used to keep track of dispensed coins. It will not try to
//  dispense coins if the coin count is zero. Returns true if
//  coin count was successfully decreased.
boolean coinsDispensed() {
  if (coinsLeft > 0) {
    --coinsLeft;
    storeCoinCount(coinsLeft);
    return true;
  }
  else {
    return false;
  }
}

// Returns the number of coins left in the machine.
int getCoinsLeft() {
  return coinsLeft;
}


