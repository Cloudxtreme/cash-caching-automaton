#include <EEPROM.h>

// Defines the EEPROM address of the stored coin count:
#define COIN_COUNT_ADDR 0 

/*
  retrieveCoinCount() reads the stored count of coins remaining in
   the machine. This value is updated when the coin count changes,
   so that it is persisted across reboots of the Arduino.
*/
int retrieveCoinCount() {
  return(EEPROM.read(COIN_COUNT_ADDR));
}

/*
  storeCoinCount() writes the given count of coins remaining in
   the machine. This value is updated when the coin count changes,
   so that it is persisted across reboots of the Arduino.
*/
void storeCoinCount(int count) {
  EEPROM.write(COIN_COUNT_ADDR, count);
}
