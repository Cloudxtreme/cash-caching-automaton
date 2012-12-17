#define FULL_AMOUNT 25 // Amount of quarters in tube to fill machine
#define SWITCH_AMOUNT 6 // Number of coins left at switch trigger

int coinsLeft = 0;

void refillCoins()
{
  coinsLeft = FULL_AMOUNT;
}

boolean coinsDispensed()
{
  if (coinsLeft > 0)
  {
    --coinsLeft;
    return true;
  }
  else
  {
    return false;
  }
}

int getCoinsLeft()
{
  return coinsLeft;
}

bool checkCoinsSwitch()
{
  return false; 
}


