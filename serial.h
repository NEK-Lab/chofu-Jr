#ifndef SERIAL_H
#define SERIAL_H

#include "setting.h"

class serial {
  private:
    String inputString;  // To hold incoming data
    boolean stringComplete; // If the string is complete

  public:
    serial() : inputString(""), stringComplete(false) {}

    void begin() {
      Serial.begin(COMSPEED);
      while (!Serial) {
        // Wait for the serial port to open
      }
    }

    void update() {
      // Read incoming serial data
      while (Serial.available() > 0) {
        char incomingChar = Serial.read();
        if (incomingChar == '\n') {
          // End of line, process the input string
          parseInput();
          inputString = ""; // Clear the input string
        } else {
          inputString += incomingChar; // Append character to input string
        }
      }
    }

  private:
    void parseInput() {
      int index = 0;
      int startIndex = 0;
      
      // Parse comma-separated values
      while (index < CONTENTS && startIndex < inputString.length()) {
        int commaIndex = inputString.indexOf(',', startIndex);
        if (commaIndex == -1) {
          commaIndex = inputString.length();
        }

        // Extract and convert substring to integer
        String value = inputString.substring(startIndex, commaIndex);
        logicoolstate[index] = value.toInt();
        startIndex = commaIndex + 1;
        index++;
      }

      // Optionally print the received values for debugging
      for (int i = 0; i < CONTENTS; i++) {
        Serial.print(logicoolstate[i]);
      }
      Serial.println();
    }
};

#endif
