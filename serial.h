#ifndef SERIAL_H
#define SERIAL_H

#include "setting.h"

class serial {
  private:
    String inputString;
    boolean stringComplete;

  public:
    serial() : inputString(""), stringComplete(false) {}

    void begin() {
      Serial.begin(COMSPEED);
      delay(2000);
      while (!Serial) {
      }
      while (Serial.available() == 0){
        Serial.read();
      } 
    }

    void update() {
      while (Serial.available() > 0) {
        char incomingChar = Serial.read();
        if (incomingChar == '\n') {
          parseInput();
          inputString = "";
        } else {
          inputString += incomingChar;
        }
      }
    }

  private:
    void parseInput() {
      int index = 0;
      int startIndex = 0;
      while (index < CONTENTS && startIndex < inputString.length()) {
        int commaIndex = inputString.indexOf(',', startIndex);
        if (commaIndex == -1) {
          commaIndex = inputString.length();
        }
        String value = inputString.substring(startIndex, commaIndex);
        logicoolstate[index] = value.toInt();
        startIndex = commaIndex + 1;
        index++;
      }
      /*for (int i = 0; i < CONTENTS; i++) {
        Serial.print(logicoolstate[i]);
      }
      Serial.println();
      */
    }
};

#endif
