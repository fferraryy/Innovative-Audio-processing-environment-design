#include <stdio.h>
#include "moving_average.h"

int main()
{
	float inputArray[10] = {0.0f, 1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 7.0f, 8.0f, 9.0f}; // Define input array
	int inputLength = 10;	// Length of input array
	float actualOutput[10] = {-1.0f, -1.0f, -1.0f, -1.0f, -1.0f, -1.0f, -1.0f, -1.0f, -1.0f, -1.0f}; // Actual output array
	
	float correctOutput[10] = {0.0f, 0.5f, 1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 7.0f, 8.0f};	// Correct output array
	
	movingAverage(3, inputArray, inputLength, actualOutput); // Call the movingAverage function
	
	// Check if actual output matches correct output
	int passed = 1;
	for(int i = 0; i < 10; i++)
	{
		if(actualOutput[i] != correctOutput[i])
		{
			passed = 0;
		}
	}

	// Print the test result
	if(passed == 1)
	{
		printf("Moving average works sucessfully.\n");
	}
	else
	{
		printf("Moving average failed test.\n");
	}
	return 0;
}
