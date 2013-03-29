// This file contains code that is used to monitor and control
// the temperature of the nearby vending machine.

#include <OneWire.h>
#include <DallasTemperature.h>
#include <EEPROM.h>

#define ONE_WIRE_BUS   2 // Data wire from temp sensor
#define RELAY_COMP_PIN 4 // Relay to control the compressor

#define CENTER_TEMP_LOC 100 // Location in EEPROM to store center
#define DELTA_TEMP_LOC  104 // Location in EEPROM to store delta

// Union used to convert between float and raw bytes:
union FloatToBytes
{  
   float f;  
   unsigned char b[sizeof(float)];  
};

// Center-point for desired temperature (°C)
float centerTemp;   
// Wiggle-room for temperature variation (+/-°C)
float deltaTemp;  

// Setup a oneWire instance to communicate with the OneWire device
OneWire oneWire(ONE_WIRE_BUS);
// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

// Setup the temperature conrol system. Should be done once at the
// start of the program.
void initTempControl(void) {
  // Read the temperature center-point value from EEPROM:
  centerTemp = readFloat(CENTER_TEMP_LOC);
  // Read the temperature delta-value from EEPROM:
  deltaTemp = readFloat(DELTA_TEMP_LOC);
  // Set the relay pin to an output:
  pinMode(RELAY_COMP_PIN, OUTPUT);
  // Make sure the relay is turned off
  digitalWrite(RELAY_COMP_PIN, LOW);
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
  
  if(temperature > centerTemp + deltaTemp) {
    digitalWrite(RELAY_COMP_PIN, HIGH);
    printDebug("Compressor activated.\r\n");
  }
  else if (temperature < centerTemp - deltaTemp) {
    digitalWrite(RELAY_COMP_PIN, LOW);
    printDebug("Compressor not activated.\r\n");
  }
  
  return temperature;
}

//Saves a floating-point value to EEPROM:
void saveFloat(float value, unsigned int loc) {
  union FloatToBytes x;
  x.f = value;
  for(int i=0; i<sizeof(float); ++i)
  {
    EEPROM.write(loc+i, x.b[i]);
  }
}

//Reads a floating-point value from EEPROM:
float readFloat(unsigned int loc) {
  union FloatToBytes x;
  for(int i=0; i<sizeof(float); ++i)
  {
    x.b[i] = EEPROM.read(loc);
  }
  return x.f;
}

/*
  Command: "set temp-center"
  Action: Sets the center-point for desired temperature in °C
*/
void setTempCenter(float value) {
  // Save the value to EEPROM first:
  saveFloat(value, CENTER_TEMP_LOC);
  // Then set the running value:
  centerTemp = value;
}

/*
  Command: "get temp-center"
  Action: Gets the center-point for desired temperature in °C
*/
float getTempCenter() {
  return centerTemp;
}

/*
  Command: "set temp-delta"
  Action: Sets the delta-value for temperature in °C
*/
void setTempDelta(float value) {
  // Save the value to EEPROM first:
  saveFloat(value, DELTA_TEMP_LOC);
  // Then set the running value:
  deltaTemp = value;
}

/*
  Command: "get temp-delta"
  Action: Gets the delta-value for temperature in °C
*/
float getTempDelta() {
  return deltaTemp;
}
