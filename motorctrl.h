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
    int xymap(double speed) {
      return int(MTPLSSTOP + (speed * MTPLSRANGE));
    }

    int zmap(double speed) {
      return int(speed * L298NPLSWIDTH);
    }

    void velscale() {
      double maxval = abs(velocity[0]);
      for (int i = 1; i < 4; i++) {
          if (abs(velocity[i]) > maxval) {
              maxval = abs(velocity[i]);
          }
      }
      if (maxval > 0) {
          for (int i = 0; i < 4; i++) {
              velocity[i] = velocity[i] / maxval;
          }
      }
    }

    void omuni(){
      veccomp[0] = axval[2];
      veccomp[1] = axval[3];
      veccomp[2] = zval;
      veccomp[3] = axval[0];
      angle_rad = atan2(veccomp[1], veccomp[0]);
      for (int i = 0; i < 6; i++) {
        velocity[i] = (thvec[i][0]*veccomp[0] + thvec[i][1]*veccomp[1] + thvec[i][2]*veccomp[2] + thvec[i][3]*veccomp[3]);
      }
      velscale();
      for (int i = 1; i < 4; i++) {
        thval[i] = xymap(velocity[i]);
      }
      th1.writeMicroseconds(thval[0]);
      th2.writeMicroseconds(thval[1]);
      th3.writeMicroseconds(thval[2]);
      th4.writeMicroseconds(thval[3]);
      for (int i = 0; i < 2; i++) {
        thval[i+4] = zmap(velocity[i+4]);
        analogWrite(THRUSTERPIN[i+9], thval[i+4]);
      }
      if (veccomp[2] > 0){
        digitalWrite(THRUSTERPIN[4], HIGH);
        digitalWrite(THRUSTERPIN[5], LOW);
        digitalWrite(THRUSTERPIN[6], HIGH);
        digitalWrite(THRUSTERPIN[7], LOW);
      }else if(veccomp[2] < 0){
        digitalWrite(THRUSTERPIN[4], LOW);
        digitalWrite(THRUSTERPIN[5], HIGH);
        digitalWrite(THRUSTERPIN[6], LOW);
        digitalWrite(THRUSTERPIN[7], HIGH);
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
      for (int i = 0; i < 4; i++) { 
        axval[i] = map(logicoolstate[i], AXMIN, AXMAX, -1, 1);
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