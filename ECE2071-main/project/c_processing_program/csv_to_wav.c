// The file csv_to_wav is to read data from csv file and write them into wav file. 

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define SAMPLE_RATE 4000
#define SAMPLE_T int16_t

typedef struct
{
	char riff[4];
	int32_t fileSize;
	char wave[4];
	char fmt[4];
	int32_t chunkSize;
	int16_t formatTag;
	int16_t numberOfChanels;
	int32_t sampleRate;
	int32_t bytesPerSecond;
	int16_t bytesPerSample;
	int16_t bitsPerSample;
	char data[4];
	int32_t dataLength;
} WAVHeader;

int main(int argc, char** argv) 
{
	if(argc != 3)
	{
		printf("Error: must provide exactly two command line argument. Firstly the file contain the numeric data and secondly the wav file output.\n");
		return 1;
	}
	const char* fInputName = argv[1];
	const char* fOutputName = argv[2];
	if(access(fInputName, F_OK) != 0)
	{
		printf("Error: the data file you have requested does not exist.\n");
		return 1;
	}
	if(access(fInputName, R_OK) != 0)
	{
		printf("Error: You do not have read permission for the data file.\n");
		return 1;
	}
	if(access(fOutputName, F_OK) == 0)
	{
		if(access(fOutputName, W_OK) != 0)
		{
			printf("Error: You do not have write permission for the wav file.\n");
			return 1;
		}
	}

	FILE* fInput = fopen(fInputName, "r");
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
	char* data = (char*)malloc((long unsigned int)(fileSize + 1)); 
	data[fileSize] = '\0'; 
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
		return 1;
	}
	
	if(sizeof(SAMPLE_T) != 2)
	{
		printf("Warning: sizeof(SAMPLE_T)=%d\n", sizeof(SAMPLE_T));
	}
	
	int32_t numSamples = 0;
	for(int i = 0; i < fileSize; i++)
	{
		if(data[i] == '\n')
		{
			numSamples++;
		}
	}
	
	SAMPLE_T* sampleData = (SAMPLE_T*)malloc(numSamples * sizeof(SAMPLE_T));
	if(sampleData == NULL)
	{
		printf("Error: could not allocate enough memory.\n");
		fclose(fInput);
		free(data);
		return 1;
	}
	
	{
		int di = 0;
		for(int si = 0; (si < numSamples) && (di < trueSize); si++)
		{
			sampleData[si] = atoi(data + di);
			sampleData[si] *= 20;
			while((data[di] != '\n') && (di < trueSize))
			{
				di++;
			}
			if(data[di] == '\n')
			{
				di++;
			}
		}
	}
	
	FILE* fOutput = fopen(fOutputName, "w");
	if(fOutput == NULL)
	{
		printf("Error: failed to open file.\n");
		return 1;
	}
	
	
	WAVHeader header;
	strncpy(header.riff, "RIFF", 4);
	header.fileSize = (numSamples * sizeof(SAMPLE_T)) + sizeof(WAVHeader);
	strncpy(header.wave, "WAVE", 4);
	strncpy(header.fmt, "fmt ", 4);
	header.chunkSize = 16;
	header.formatTag = 1;
	header.numberOfChanels = 1;
	header.sampleRate = SAMPLE_RATE;
	header.bytesPerSecond = SAMPLE_RATE * sizeof(SAMPLE_T);
	header.bytesPerSample = sizeof(SAMPLE_T);
	header.bitsPerSample = sizeof(SAMPLE_T) * 8;
	strncpy(header.data, "data", 4);
	header.dataLength = numSamples * SAMPLE_RATE * sizeof(SAMPLE_T);
	
	
	fwrite(&header, 1, sizeof(WAVHeader), fOutput);
	fwrite(sampleData, 2, numSamples, fOutput);
	
	
	fclose(fOutput);
	
	free(data);
	free(sampleData);
	
	return 0;
}
