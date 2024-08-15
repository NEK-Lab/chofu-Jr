#include "serial.h"
#include "motorctrl.h"
#include "servoctrl.h"

serial transmit;
motorctrl thruster;
servoctrl hand;

void setup() {
  transmit.begin();
  thruster.set();
  hand.set();
}

void loop() {
  transmit.update();
  thruster.drive();
  hand.drive();
}

