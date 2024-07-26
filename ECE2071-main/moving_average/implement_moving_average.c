// The file implement_moving_average is to save the filtered data into a new file by using the movingAverage funtion.

#include <stdio.h>
#include "moving_average.h"
#include <stdlib.h>
#include <unistd.h>

#define DEFAULT_INPUT_FILE_NAME "../project/output.csv"
#define DEFAULT_OUTPUT_FILE_NAME "../project/moving_average_result.txt"

int main(int argc, char** argv)
{
	const char* inputFileName;
	const char* resultFileName;
	if(argc >= 2)
	{
		inputFileName = argv[1];
	}
	else
	{
		inputFileName = DEFAULT_INPUT_FILE_NAME;
	}
	if (argc >= 3)
	{
		resultFileName = argv[2];
	}
	else
	{
		resultFileName = DEFAULT_OUTPUT_FILE_NAME;
	}
	
	if(access(inputFileName, F_OK) != 0)
	{
		printf("Error: the data file you have requested does not exist.\n");
		return 1;
	}
	if(access(inputFileName, R_OK) != 0)
	{
		printf("Error: You do not have read permission for the data file.\n");
		return 1;
	}
	if(access(resultFileName, F_OK) == 0)
	{
		if(access(resultFileName, W_OK) != 0)
		{
			printf("Error: You do not have write permission for the wav file.\n");
			return 1;
		}
	}
	
    FILE *inputFile = fopen(inputFileName, "r");
    if(inputFile == NULL)
    {
    	printf("Error: could not open input file.\n");
    	return 1;
    }
    //count the number of lines in the file
    int numLines = 0;
    char c;
    while((c = getc(inputFile)) != EOF)
    {
    	if(c == '\n')
    	{
    		numLines++;
    	}
    }
    //go back to the start of the file
    fseek(inputFile, 0, SEEK_SET);
    
    //allocate the buffers
    float* dataArray = (float*)malloc(numLines*sizeof(float));
    if(dataArray == NULL)
    {
    	printf("Could not allocate enough memory.\n");
    	fclose(inputFile);
    	return 1;
    }
    float* filteredDataArray = (float*)malloc(numLines*sizeof(float));
    if(dataArray == NULL)
    {
    	printf("Could not allocate enough memory.\n");
    	fclose(inputFile);
    	free(dataArray);
    	return 1;
    }
     
    float data1, data2;
    int index = 0;
    int count;
    // Read data from the CSV file
    while(fscanf(inputFile, "%f,%f\n", &data1, &data2) != EOF) {
        if(index >= numLines)
        {
        	printf("Error on line %d. dataArray out of bounds.\n", __LINE__ + 6);
        	fclose(inputFile);
        	free(dataArray);
        	free(filteredDataArray);
        	return 1;
        }
        dataArray[index] = data1;
        index++;
    }
    fclose(inputFile);
    
    if(index != numLines)
    {
    	printf("Warning: number of lines and length of data miss match.\n");
    }
    
    //open result file 
    FILE *resultFile = fopen(resultFileName,"w"); 
    if (resultFile == NULL) {
        printf("Error opening the file.\n");
        free(dataArray);
        free(filteredDataArray);
        return 1;
    }

	movingAverage(5, dataArray, numLines ,filteredDataArray);
    for (int i = 0 ; i < numLines; i++) {
        if (filteredDataArray[i] > 0) //remove all empty space
        {  
            count ++; 
        }
    }
    //save filtered data in a result array 
    float result[count]; 
    for (int i = 0; i < count; i++)  {
        result[i] = filteredDataArray[i]; 
        fprintf(resultFile,"%.2f\n", result[i]);
    }
    fclose(resultFile); 
	return 0;
}
