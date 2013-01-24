//-----------------------------------------------------------------
#include <string.h>
#include <TimerOne.h>

#define RELAY_DISP_PIN  A0
#define RELAY_LIGHT_PIN A1

#define MAX_COMMAND_LENGTH  64

String inputString = "";        // String read in from serial
String lastString = "";         // Last complete string read in
boolean stringComplete = false; // Is the string finished?

void setup() {
  // Start up the serial at 9600 baud:
  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);
  digitalWrite(A0, HIGH);
  digitalWrite(A1, HIGH);
  Serial.begin(9600);
  //Serial.print(">: ");
}

void loop() {
  // Read in any serial values:
  serialEvent();
  // If a full string is read in:
  if (stringComplete) {
    // Try to parse the command:
    parseCommand();
    // Reset the stringComplete flag:
    stringComplete = false;
  }
}

/*
  serialEvent() checks for serial data and adds any new chars
   to inputString. If the stringComplete flag is true, it means
   a newline was found and the string is complete.
 */
void serialEvent() {
  while (Serial.available()) {
    // Read in the next byte (character) via serial:
    char inChar = (char)Serial.read(); 

    // If a newline is found:
    if (inChar == '\n' || inChar == '\r' || inChar == '\0') {
      // Convert the string to lowercase:
      inputString.toLowerCase();
      // The string is fully-formed, set the stringComplete flag:
      stringComplete = true;
      // Set the lastString to the new complete string:
      lastString = inputString;
      // Clear the inputString:
      inputString = "";
      // Start the next terminal line:
      //Serial.print("\n>: ");
    } 
    // Otherwise, keep going:
    else if (!stringComplete){
      // Add the character to the inputString:
      inputString += inChar;
      //Serial.print(inChar);
    }
  }
}

/*
  parseCommand() tries to analyze the string that was read in
   from serial and match it up with the corresponding function
   call.
*/
void parseCommand() {
  // Grab the first keyword from the string:
  String keyword = getNextKeyword();
  // Find the case where the keyword matches the function:
  if (keyword.equals("dispense")) {
    keyword = getNextKeyword();
    if (keyword.equals("") || keyword.equals("dispense")) {
      dispense(1);
    }
    else if (keywordIsInt(keyword)) {
      dispense(keywordToInt(keyword));
    }
    else {
      invalidKeyword(keyword);
    }
  }
  else if (keyword.equals("check")) {
    keyword = getNextKeyword();
    if (keyword.equals("tube")) {
      keyword = getNextKeyword();
      if (keywordIsInt(keyword)) {
        checkTube(keywordToInt(keyword));
      }
      else if (keyword.equals("") || keyword.equals("check")){
        Serial.println("Error: tube number not entered.");
      } 
      else {
        invalidKeyword(keyword);
      }
    } 
  }
  else if (keyword.equals("refill")) {
    refill();
  }
  else if (keyword.equals("test")) {
  }
  else if (keyword.equals("")) {
  }
  else {
    invalidKeyword(keyword);
  } 
}

/*
  getNextKeyword() pulls out and returns the next keyword from 
   the input string. Keywords are seperated by spaces and may 
   contain any type of symbol.
*/
String getNextKeyword() {
  String keyword; // Placeholder string for the current keyword
  int keywordLength; // Length of the keyword
  
  // Length of the keywoard is the same as the index of the space:
  keywordLength = lastString.indexOf(' ');
  // If the string contains no spaces (just one keyword):
  if (keywordLength == -1) {
    // The keyword is the whole string:
    keyword = lastString;
  }
  // Otherwise the string contains one or more keywords:
  else {
    // Collect the first keyword:  
    keyword = lastString.substring(0, keywordLength);
    // Remove the keyword (and space) from the string:
    lastString = lastString.substring(keywordLength + 1);
  } 
  return keyword;
}

/*
  invalidKeyword() current displays an error message stating that
   the current keyword is not valid. Future improvements may allow
   the suggestion of valid keywords that are similar.
*/
void invalidKeyword(String keyword) {
  Serial.print("Error: keyword '");
  Serial.print(keyword);
  Serial.println("' is invalid.");
}

/*
  keywordIsInt() returns 'true' if the keyword is an integer, and
   'false' if it is not.
*/
boolean keywordIsInt(String keyword) {
  bool retVal = false; // Return value
  // Convert the string to a char array:
  char cstring[keyword.length() + 1];
  keyword.toCharArray(cstring, sizeof(cstring));
  // Convert the char array to an int:
  int tempInt = atoi(cstring);
  // If the conversion results in '0' and the string is not "0":
  if (tempInt == 0 && !keyword.equals("0")) {
    // The conversion failed, not an int:
    retVal = false; 
  }
  else {
    // Otherwise, the conversion was a success:
    retVal = true;
  }
  return retVal;
}

/*
  keywordToInt() returns the converted integer value of the
   keyword. keyword should be checked with keywordIsInt() first;
   keywordToInt() will return '0' if keyword conversion fails. 
*/
int keywordToInt(String keyword) {
  // Convert the string to a char array:
  char cstring[keyword.length() + 1];
  keyword.toCharArray(cstring, sizeof(cstring));
  // Convert the char array to an int:
  return atoi(cstring);
}
