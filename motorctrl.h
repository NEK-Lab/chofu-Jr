#ifndef MOTORCTRL_H
#define MOTORCTRL_H

#include "setting.h"

#include <Servo.h>

Servo th1;
Servo th2;
Servo th3;
Servo th4;

class motorctrl {
  private:
    void velscale() {
      double maxval = abs(velocity[0]);
      for (int i = 1; i < 4; i++) {
          if (abs(velocity[i]) > maxval) {
              maxval = abs(velocity[i]);
          }
      }
      if (maxval > 0) {
          for (int i = 0; i < 4; i++) {
              velocity[i] = velocity[i] / maxval * CLUCRANGE;
          }
      }
    }

    void omuni(){
      veccomp[0] = map(axval[2], AXMIN, AXMAX, -CLUCRANGE, CLUCRANGE);
      veccomp[1] = map(axval[3], AXMIN, AXMAX, -CLUCRANGE, CLUCRANGE);
      veccomp[2] = zval;
      veccomp[3] = map(axval[0], AXMIN, AXMAX, -CLUCRANGE, CLUCRANGE);
      for (int i = 0; i < 6; i++) {
        velocity[i] = (thvec[i][0]*veccomp[0] + thvec[i][1]*veccomp[1] + thvec[i][2]*veccomp[2] + thvec[i][3]*veccomp[3]);
      }
      velscale();
      th1.writeMicroseconds(map(velocity[0], -CLUCRANGE, CLUCRANGE, MTPLSMIN, MTPLSMAX));
      th2.writeMicroseconds(map(velocity[1], -CLUCRANGE, CLUCRANGE, MTPLSMIN, MTPLSMAX));
      th3.writeMicroseconds(map(velocity[2], -CLUCRANGE, CLUCRANGE, MTPLSMIN, MTPLSMAX));
      th4.writeMicroseconds(map(velocity[3], -CLUCRANGE, CLUCRANGE, MTPLSMIN, MTPLSMAX));
      if (veccomp[2] == 1){
        analogWrite(THRUSTERPIN[9],255);
        analogWrite(THRUSTERPIN[10],255);
        digitalWrite(THRUSTERPIN[4], HIGH);
        digitalWrite(THRUSTERPIN[5], LOW);
        digitalWrite(THRUSTERPIN[6], HIGH);
        digitalWrite(THRUSTERPIN[7], LOW);
      }else if(veccomp[2] == -1){
        analogWrite(THRUSTERPIN[9],255);
        analogWrite(THRUSTERPIN[10],255);
        digitalWrite(THRUSTERPIN[4], LOW);
        digitalWrite(THRUSTERPIN[5], HIGH);
        digitalWrite(THRUSTERPIN[6], LOW);
        digitalWrite(THRUSTERPIN[7], HIGH);
      }else{
        analogWrite(THRUSTERPIN[9],0);
        analogWrite(THRUSTERPIN[10],0);
      }
    }
    
  public:
    void set(){
      th1.attach(THRUSTERPIN[0]);
      th2.attach(THRUSTERPIN[1]);
      th3.attach(THRUSTERPIN[2]);
      th4.attach(THRUSTERPIN[3]);
      pinMode(THRUSTERPIN[4], OUTPUT);
      pinMode(THRUSTERPIN[5], OUTPUT);
      pinMode(THRUSTERPIN[6], OUTPUT);
      pinMode(THRUSTERPIN[7], OUTPUT);
      pinMode(THRUSTERPIN[8], OUTPUT);
      digitalWrite(THRUSTERPIN[8], HIGH);
      pinMode(THRUSTERPIN[9], OUTPUT);
      pinMode(THRUSTERPIN[10], OUTPUT);
      for (int i = 0; i < 4; i++) {
        veccomp[i] = 0;
      }
      zval = 0;
    }

    void drive(){
      for (int i = 0; i < 4; i++){
        axval[i] = logicoolstate[i];
      }
      if(logicoolstate[8] == 1){
        zval = 1;
      }else if(logicoolstate[10] == 1){
        zval = -1;
      }else{
        zval = 0;
      }
      omuni();
    }
};
#endif