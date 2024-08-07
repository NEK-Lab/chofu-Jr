#include "serial.h"
#include "motorctrl.h"

serial transmit;
motorctrl thruster;

void setup() {
  transmit.begin();
  thruster.set();
}

void loop() {
  transmit.update();
  thruster.drive();
}

