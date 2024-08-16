#pragma once

#include <math.h>

const int COMSPEED = 9600;
const int DIGITS = 28;
const unsigned int CONTENTS = 20;

int logicoolstate[20];
//LX,LY,RX,RY,X,A,B,Y,LB,RB,LT,RT,BACK,START,LS,RS,HATX,HATY,0,0

const int AXMAX = 255;
const int AXMIN = -255;


const int THRUSTERPIN[11] = {3,2,13,12,6,7,4,5,10,9,8};//rf,lf,lb,rb,rzA,rzB,lzA,lzB,STBY,rzPWM,lzPWM
const int MTPLSMAX = 2000;
const int MTPLSMIN = 1000;
const int MTPLSSTOP = 1500;
const int MTPLSRANGE = 500;

const int L298NPLSWIDTH = 255;

const int CLUCRANGE = 1000;

double axval[4];//lx,ly,rx,ry
double zval;
double veccomp[4];//x,y,z,r
double angle_rad;

double thvec[6][4] = {
    {(-sin(M_PI/4)),  (cos(M_PI/4)),  0, -0.5},
    {-(-cos(M_PI/4)), -(-sin(M_PI/4)), 0,  0.5},
    {-(sin(M_PI/4)),  -(-cos(M_PI/4)),  0,  0.5},
    {(cos(M_PI/4)),   (sin(M_PI/4)), 0, -0.5},
    {0, 0, 1, 0},
    {0, 0, 1, 0}
};

int velocity[6];
int thval[6];

const int SVPIN = 11;
const int SVPLSMAX = 1970;//close hand
const int SVPLSMIN = 1050;//open hand
const int HANDSPEED = 50;

int currenthand;
