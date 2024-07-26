#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>

#define INPUT_FILE_NAME "output.temp"
#define OUTPUT_FILE_NAME "output.DATA"

#define CHUNK_SIZE 6250
#define CHUNK_ARRAY_LENGTH 9375
#define SIZE_OF_SAMPLE 2
#define SAMPLE_TIME 160
#define SIZE_OF_COUNT 4
#define CHUNK_DISK_SPACE (CHUNK_ARRAY_LENGTH + SIZE_OF_COUNT)
#define LOWER_PACK_MASK 0x00000FFF
#define UPPER_PACK_MASK 0x00FFF000
#define UPPER_PACK_OFFSET 12

int main()
{
	if(access(INPUT_FILE_NAME, F_OK) != 0)
	{
		printf("Error: the temp file you have requested does not exist.\n");
		return 1;
	}
	if(access(INPUT_FILE_NAME, R_OK) != 0)
	{
		printf("Error: You do not have read permission for the temp file.\n");
		return 1;
	}
	if(access(OUTPUT_FILE_NAME, F_OK) == 0)
	{
		if(access(OUTPUT_FILE_NAME, W_OK) != 0)
		{
			printf("Error: You do not have write permission for the data file.\n");
			return 1;
		}
	}
	
	FILE* fInput = fopen(INPUT_FILE_NAME, "r");
	if(fInput == NULL)
	{
		printf("Error: failed to open file.\n");
		return 1;
	}
	//get the size of the file
	fseek(fInput, 0, SEEK_END);
	long fileSize = ftell(fInput);
	if(fileSize == 0)
	{
		printf("Error: file is empty.\n");
		fclose(fInput);
		return 1;
	}
	fseek(fInput, 0, SEEK_SET);
	
	char* data = (char*)malloc((long unsigned int)(fileSize));
	if(data == NULL)
	{
		printf("Error: could not allocate enough memeory.\n");
		fclose(fInput);
		return 1;
	}
	size_t trueSize = fread(data, 1, fileSize, fInput); // Read data from fInput and save the number of bytes in trueSize
	fclose(fInput);
	if((long)trueSize != fileSize) 
	{
		printf("Error: could not read entire file");
		free(data);
		return 1;
	}
	
	long numChunks = fileSize / CHUNK_DISK_SPACE;
	uint16_t* output = (uint16_t*)malloc(numChunks * CHUNK_SIZE * sizeof(uint16_t));
	if(output == NULL)
	{
		printf("Error: could not allocate enough memeory.\n");
		free(data);
		return 1;
	}
	
	char* dataPointer = data;
	int outputIndex = 0;
	for(int i = 0; i < numChunks; i++)
	{
		int numElements = *((int*)dataPointer);
		dataPointer += SIZE_OF_COUNT;
		for(int j = 0; j < numElements; j+=2)
		{
			int val1 = (*((uint32_t*)dataPointer)) & LOWER_PACK_MASK;
			int val2 = ((*((uint32_t*)dataPointer)) & LOWER_PACK_MASK) >> UPPER_PACK_OFFSET;
			output[outputIndex] = val1;
			output[outputIndex + 1] = val2;
			dataPointer += 3;
		}
	}
	
	FILE* fOutput = fopen(OUTPUT_FILE_NAME, "w");
	if(fOutput == NULL)
	{
		printf("Error: failed to open file.\n");
		free(data);
		free(output);
		return 1;
	}
	for(int i = 0; i < (numChunks * CHUNK_SIZE); i++)
	{
		fprintf(fOutput, "%d,%d\n", output[i], SAMPLE_TIME);
	}
	fclose(fOutput);

	free(data);
	free(output);
	return 0;
}
