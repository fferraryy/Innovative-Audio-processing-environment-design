// The file moving_average is to calculate the moving average of input array and store the result in destination array,
// in order to reduce the noise in data.
#include "moving_average.h"
//get input from csv 
//window = 5 
//data is inputarray
void movingAverage(int windowLength, float* inputArray, int inputLength, float* destinationArray)
{
	float movingWindow = 0.0f; // Initialize a variable to store  values
	for(int i = 0; i < windowLength; i++) // Go through the whole movingWindow
	{
		movingWindow += inputArray[i]; // Assign the value into movingWindow
		destinationArray[i] = movingWindow / (float)(i + 1); // Calculate average
	}
	// Calculate the moving average for the remaining elements using a sliding window approach
	float oneOnN = 1.0f / windowLength; 
	for(int i = windowLength; i < inputLength; i++)
	{
		movingWindow += inputArray[i];
		movingWindow -= inputArray[i - windowLength]; // Subtract the oldest value from the moving window
		destinationArray[i] = movingWindow * oneOnN; //Store in the destination array
	}
}
