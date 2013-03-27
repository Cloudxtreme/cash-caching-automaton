// This file contains code that is used to monitor and control
// the temperature of the nearby vending machine.

#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 12 // Data wire from temp sensor
#define RELAY_PIN    4 // Relay to control the compressor

// Center-point for desired temperature (°C)
#define TEMP_CENTER 2   
// Wiggle-room for temperature variation (+/-°C)
#define TEMP_DELTA  0.5  

// Setup a oneWire instance to communicate with the OneWire device
OneWire oneWire(ONE_WIRE_BUS);
// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

// Setup the temperature conrol system. Should be done once at the
// start of the prpgram.
void initTempControl(void) {
  // Set the relay pin to an output:
  pinMode(RELAY_PIN, OUTPUT);
  // Make sure the relay is turned off
  digitalWrite(RELAY_PIN, LOW);
  // Start up the temperature library
  sensors.begin();
}

//Take a temperature measurement and toggle the relay that controls
// the compressor if needed. Returns the current temperature in °C.
float runTempControl(void) { 
  
  // Send the command to get the current temperature:
  printDebug("Reading temperature... ");
  sensors.requestTemperatures(); 
  printDebug("Done.");
  
  float temperature = sensors.getTempCByIndex(0);
  printDebug("Temperature: ");
  printDebug(temperature);  
  printDebug("°C\r\n");
  
  if(temperature > TEMP_CENTER + TEMP_DELTA) {
    digitalWrite(RELAY_PIN, HIGH);
    printDebug("Compressor activated.\r\n");
  }
  else if (temperature < TEMP_CENTER - TEMP_DELTA) {
    digitalWrite(RELAY_PIN, LOW);
    printDebug("Compressor not activated.\r\n");
  }
  
  return temperature;
}
