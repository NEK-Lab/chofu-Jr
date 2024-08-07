#ifndef MOTORCTRL_H
#define MOTORCTRL_H

#include "setting.h"

#include <Servo.h>

Servo mt1;
Servo mt2;
Servo mt3;
Servo mt4;

class motorctrl {
  private:
    int conv(int in){
      int out = map(in, AXMIN, AXMAX, MTPLSMIN, MTPLSMAX);
      return out;
    }

    void rot(int val[4]){
      for (int i = 0; i < 4; i++) {
        mtval[i] = conv(val[i]);
      }
      mt1.writeMicroseconds(mtval[0]);
      mt2.writeMicroseconds(mtval[1]);
      mt3.writeMicroseconds(mtval[2]);
      mt4.writeMicroseconds(mtval[3]);
    }
    
  public:
    void set(){
      mt1.attach(MOTORPIN[0]);
      mt2.attach(MOTORPIN[1]);
      mt3.attach(MOTORPIN[2]);
      mt4.attach(MOTORPIN[3]);

    }

    void drive(){
      for (int i = 0; i < 4; i++) {
        axval[i] = logicoolstate[i];
      }
      rot(axval);
    }

};
#endif