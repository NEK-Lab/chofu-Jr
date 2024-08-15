#ifndef SERVOCTRL_H
#define SERVOCTRL_H

#include "setting.h"

#include <Servo.h>

Servo h1;

class servoctrl {
  private:
    void move(int val){
      currenthand += val;
      h1.writeMicroseconds(currenthand);
    }

    void absopen(){
      currenthand = SVPLSMIN;
      h1.writeMicroseconds(SVPLSMIN);
    }

    void absclose(){
      currenthand = SVPLSMAX;
      h1.writeMicroseconds(SVPLSMAX);
    }

  public:
    void set(){
      h1.attach(SVPIN);
      absclose();
      delay(1000);
      absopen();
    }

    void drive(){
      if(logicoolstate[5] == 1){
        absopen();
      }else if(logicoolstate[6] == 1){
        absclose();
      }
    }

};

#endif
