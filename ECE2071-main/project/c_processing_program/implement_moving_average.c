// The file implement_moving_average is to save the filtered data into a new file by using the movingAverage funtion.

#include <stdio.h>
#include "moving_average.h"
#include <stdlib.h>
#include <unistd.h>

#define DEFAULT_INPUT_FILE_NAME "python_interface_and_output_file/output.DATA"
#define DEFAULT_OUTPUT_FILE_NAME "python_interface_and_output_file/moving_average_result.csv"

int main(int argc, char** argv)
{
    const char* inputFileName;
    const char* resultFileName;
    if (argc >= 2)
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

    if (access(inputFileName, F_OK) != 0)
    {
        printf("Error: the data file you have requested does not exist.\n");
        return 1;
    }
    if (access(inputFileName, R_OK) != 0)
    {
        printf("Error: You do not have read permission for the data file.\n");
        return 1;
    }
    if (access(resultFileName, F_OK) == 0)
    {
        if (access(resultFileName, W_OK) != 0)
        {
            printf("Error: You do not have write permission for the result file.\n");
            return 1;
        }
    }

    FILE* inputFile = fopen(inputFileName, "r");
    if (inputFile == NULL)
    {
        printf("Error: could not open input file.\n");
        return 1;
    }

    // Count the number of lines in the file
    int numLines = 0;
    char c;
    while ((c = getc(inputFile)) != EOF)
    {
        if (c == '\n')
        {
            numLines++;
        }
    }
    // Go back to the start of the file
    fseek(inputFile, 0, SEEK_SET);

    // Allocate the buffers with initial capacity
    int capacity = numLines; // Initial capacity
    float* dataArray = (float*)malloc(capacity * sizeof(float));
    float* filteredDataArray = (float*)malloc(capacity * sizeof(float));
    if (dataArray == NULL || filteredDataArray == NULL)
    {
        printf("Could not allocate enough memory.\n");
        fclose(inputFile);
        return 1;
    }

    float data1;
    int index = 0;
    // Read data from the CSV file
    while (fscanf(inputFile, "%f,\n", &data1) != EOF) //the format is to be changed to also read time 
    {
        // Check if the index exceeds the current capacity
        if (index >= capacity)
        {
            // Increase the capacity by doubling it
            capacity *= 2;
            float* tempArray = (float*)realloc(dataArray, capacity * sizeof(float));
            if (tempArray == NULL)
            {
                printf("Could not allocate enough memory.\n");
                fclose(inputFile);
                free(dataArray);
                free(filteredDataArray);
                return 1;
            }
            dataArray = tempArray;

            tempArray = (float*)realloc(filteredDataArray, capacity * sizeof(float));
            if (tempArray == NULL)
            {
                printf("Could not allocate enough memory.\n");
                fclose(inputFile);
                free(dataArray);
                free(filteredDataArray);
                return 1;
            }
            filteredDataArray = tempArray;
        }

        dataArray[index] = data1;
        index++;
    }
    fclose(inputFile);

    // Perform moving average
    movingAverage(5, dataArray, numLines, filteredDataArray);

    // Open result file for writing
    FILE* resultFile = fopen(resultFileName, "w");
    if (resultFile == NULL)
    {
        printf("Error opening the result file.\n");
        free(dataArray);
        free(filteredDataArray);
        return 1;
    }

    // Write filtered data to result file
    for (int i = 0; i < numLines; i++)
    {
        fprintf(resultFile, "%.2f\n", filteredDataArray[i]); 
    }

    fclose(resultFile);
    free(dataArray);
    free(filteredDataArray);
    return 0;
}
