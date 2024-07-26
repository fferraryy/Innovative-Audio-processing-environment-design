# The file read_from_uart is to read and display the data from uart

import serial
import sys
from serial_disk import getvalidPorts

# Determine the serial port to use
port = None
if len(sys.argv) == 2:
	port = sys.argv[1]
else:
	ports = getvalidPorts() # Call getvalidPorts function
	if len(ports) == 0:
		print("There are no available ports")
		quit()
	print("The available ports are:")

	# For loop to iterate over both the indices and the values of the list simultaneously
	for i,p in enumerate(ports): # set i as the index of the current element in the ports list, 
								 # and p as the value of the current element
		print(f"{i}. {p}") # Display available ports with their corresponding index
	
	# Read from the serial port until a newline or null byte is encountered
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
	


s = serial.Serial(port, baudrate=115200)
# Continuously read and print data from the serial port until interrupted
while True:
	c = s.read(1)
	if c == b'\n': break
	if c == b'\x00': break
try:
	while True:
		try:
			data = s.read(1)
			while data[-1] != ord('\n'):
				data += s.read(1)
			print(data.decode("utf-8").strip())
		except UnicodeDecodeError:
			pass
except KeyboardInterrupt:
	print("\nClosing port")
	s.close()
