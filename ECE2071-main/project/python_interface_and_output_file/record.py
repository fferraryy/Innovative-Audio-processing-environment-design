# The file record is to record data from STM32

import serial
import sys
from serial_disk import getvalidPorts
import matplotlib.pyplot as plt

CHUNK_SIZE = 4000
SIZE_OF_SAMPLE = 2
SAMPLE_TIME = 250
FILE_NAME = "output.DATA"

# Function recordFromSTM is to record data from STM32
def recordFromSTM(port, baud=115200, duration=300):
	buff = ""
	data = [None] * CHUNK_SIZE
	output = ""
	s = serial.Serial(port, baudrate=baud) # connect serial
	
	for _ in range(duration):
		while True:
			while s.read(1) != b'\xff': # Wait for start of data packet
				pass
			if s.read(7) == b'\xee\xdd\xcc\xbb\xaa\x00\xff':
				break
		try:
			num = s.read(4) # Read the number of values in the chunk
			num = int.from_bytes(num[::-1])
			for i in range(CHUNK_SIZE):
				data[i] = int.from_bytes(s.read(SIZE_OF_SAMPLE)[::-1])
			for d in data:
				output += f"{d},{SAMPLE_TIME}\n"
		except KeyboardInterrupt:
			break
		
	# Write data to output file
	with open(FILE_NAME, "w") as f:
		f.write(output)
	s.close()
	
if __name__ == "__main__":
	# Process command line arguments
	port = None
	baud = 115200
	duration = 0
	if len(sys.argv) == 2:
		if sys.argv[1].startswith("baud="): # if the argument starts with baud=
			baud = int(sys.argv[1][5:]) # assign baud to be the integer extracts the substring from the 6th character to the end
		elif sys.argv[1].startswith("port="):
			port = sys.argv[1][5:]
		elif sys.argv[1].startswith("duration="):
			duration = int(sys.argv[1][9:])
		else:
			print(f"Invalid argument {sys.argv[1]}.")
			quit()
	if len(sys.argv) == 3:
		if sys.argv[2].startswith("baud="):
			baud = int(sys.argv[2][5:])
		elif sys.argv[2].startswith("port="):
			port = sys.argv[2][5:]
		elif sys.argv[2].startswith("duration="):
			duration = int(sys.argv[2][9:])
		else:
			print(f"Invalid argument {sys.argv[2]}.")
			quit()
	if len(sys.argv) == 4:
		if sys.argv[3].startswith("baud="):
			baud = int(sys.argv[3][5:])
		elif sys.argv[3].startswith("port="):
			port = sys.argv[3][5:]
		elif sys.argv[3].startswith("duration="):
			duration = int(sys.argv[3][9:])
		else:
			print(f"Invalid argument {sys.argv[2]}.")
			quit()

	if port == None:
		ports = getvalidPorts()
		if len(ports) == 0:
			print("There are no available ports")
			quit()
		print("The available ports are:")
		for i,p in enumerate(ports):
			print(f"{i}. {p}")
		while True:
			portNum = input("please enter the number of the port you want to use: ")
			if portNum == "":
				portNum = 0
			try:
				portNum = int(portNum)
				break
			except:
				print(f"invalid choice {portNum}. Please try again\n")
		port = ports[portNum]
	
	recordFromSTM(port, baud, duration)
