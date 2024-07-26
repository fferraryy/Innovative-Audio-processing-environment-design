#ifndef MOVING_AVERAGE_HEADER
#define MOVING_AVERAGE_HEADER

#include <stdio.h>

void movingAverage(int windowLength, float* inputArray, int inputLength, float* destinationArray);

#ifndef MOVING_AVERAGE_SINGLE_FILE_INCLUDE_DONE
#ifdef MOVING_AVERAGE_SINGLE_FILE_INCLUDE
#define MOVING_AVERAGE_SINGLE_FILE_INCLUDE_DONE
#include "moving_average.c"
#endif //MOVING_AVERAGE_SINGLE_FILE_INCLUDE
#endif //MOVING_AVERAGE_SINGLE_FILE_INCLUDE_DONE

#endif //MOVING_AVERAGE_HEADER
