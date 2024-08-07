#pragma once

#include <math.h>

const int COMSPEED = 9600;
const int DIGITS = 28;
const unsigned int CONTENTS = 20;

int logicoolstate[20];

const int AXMAX = 255;
const int AXMIN = -255;


const int MOTORPIN[4] = {4,5,6,7};

const int MTPLSMAX = 1900;
const int MTPLSMIN = 1100;
const int MTPLSSTOP = 1500;

int axval[4];

int mtval[4];