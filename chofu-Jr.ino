#include "serial.h"
#include "motorctrl.h"
#include "servoctrl.h"

serial transmit;
motorctrl thruster;
servoctrl hand;

void(* resetFunc) (void) = 0;

void setup() {
  transmit.begin();
  thruster.set();
  hand.set();
}

void loop() {
  transmit.update();
  thruster.drive();
  hand.drive();
  /*if (logicoolstate[14] == 1 && logicoolstate[15] == 1){
    resetFunc();
  }*/
}

