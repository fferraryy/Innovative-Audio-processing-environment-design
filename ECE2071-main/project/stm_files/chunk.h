#ifndef CHUNK_HEADER_GUARD
#define CHUNK_HEADER_GUARD

#define CHUNK_SIZE 4000
#define SAMPLE_TIME 250

//struct holding one second of data
typedef struct {
	uint64_t syncGuard;
	uint32_t numValues;
	uint16_t data[CHUNK_SIZE];
} Chunk;

#endif
