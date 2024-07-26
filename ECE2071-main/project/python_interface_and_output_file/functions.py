# The file functions is the collection of all functions that can be used in main_interface.py

import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import time
from random import random
import numpy as np
import matplotlib.pyplot as plt
import csv
import time 
import pygame
import subprocess
import os


# Function play_audio is to play audio from the WAV file 
def play_audio(file): 
	try: 
		pygame.mixer.init()
		pygame.mixer.music.load(file)
		pygame.mixer.music.play()
	except pygame.error: 
		print("Error opening file")

# Function generate_graph is to generate and display a graph from the data in the output CSV file.
def generate_graph_csv(filename, outName): 
	dataList = []
	count = 0
	try: 
		with open(filename, newline='') as csvfile:
            # Create a CSV reader object
			csvReader = csv.reader(csvfile)
            # Iterate over each row in the CSV file
			for row in csvReader:
                # Each row is a list of values
				data = float(row[0])
                # Calibrate data 
				caliData = (data/4096)*3
				dataList.append(caliData)
				count += 1 
            
        # Set the number of points in 1 sec
		time_interval = 1 / 2500
        # Series of time
		time = np.arange(0, count * time_interval, time_interval)
        # Plotting
		plt.plot(time, dataList, '-', color='b', markersize=0.05)
		plt.title('Voltage vs Time')
		plt.xlabel('Time (s)')
		plt.xticks(np.arange(0, count * time_interval + 1, 1))
		plt.ylabel('Voltage (V)')
		plt.grid(True)
        
        # Save the plot
		plt.savefig(outName)
        
        # Show the plot
		plt.show()
        
        # Close the plot window
		plt.close()

	except FileNotFoundError: 
		print("File not found")
	except AttributeError: 
		print("...exit mode...")


# Function get_time_duration is to calculate the duration of the time based on the timestamps in the CSV file.
def get_time_duration(): 
	# Open the CSV file in read mode
	with open('../python_interface_and_output_file/output.DATA', newline='') as csvfile:
    	# Create a CSV reader object
		csvReader = csv.reader(csvfile)
		duration = 0 #initialise time duration 
    	# Iterate over each row in the CSV file
		for row in csvReader:
        # Each row is a list of values
			timeInterval = int(row[-1])
			duration = duration + timeInterval 
	#convert to second 
	duration = duration/1000 
	return duration 


# def write_data_file(distance): 
# 	print("\n..detecting distance..")
# 	file = open("../python_interface_and_output_file/DATA.txt","w")
# 	file.write("distance : {}\n".format(distance))
# 	file.close


# # Function write_data_file is to write data to a file based on certain conditions.
# def write_data_file(minDistance,maxDistance): 
# 	print("..detecting distance..")
# 	file = open("python_interface_and_output_file/DATA.txt","w")
# 	# distance = read_from_uart() #need uart to return distance
# 	distance = random() #for testing 
# 	if distance < maxDistance and distance > minDistance: 
# 		while True: 
# 			print("distance form the user is in the range")
# 			file.write("distance : {}\n".format(distance))
# 			time.sleep(1)
# 	else: 
# 		print("user is farer than 10cm")
# 		print("...stop recording..")

# 	file.close



# Function get_ports is to seach for available ports, return name of the ports.
def get_ports(): 
    ports = serial.tools.list_ports.comports()
    return ports


# Function findSTM32 is to find the connection with STM32, take all available ports and find which one is connected to STM32
# return port connected to STM32 
def findSTM32(portsFound): 
    commPort = 'None'
    numPort = len(portsFound)

    for i in range(0,numPort): 
        port = portsFound[i]
        strPort = str(port)
        #print(strPort)
        if 'STM32' in strPort: 
            splitPort = strPort.split(' ')
            print(splitPort)
            commPort = (splitPort[0])
    return commPort


# Function read_from_uart is to read data/signal recieved from STM32 used with US
# return distance 
def read_from_uart(connectedPort): 
	print("\n...Data is being transmitted from STM32...")
	s = serial.Serial(connectedPort,115200)
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
				decoded_data = data.decode("utf-8").strip()
				
			except UnicodeDecodeError:
				pass
	except KeyboardInterrupt:
		s.close()
	return decoded_data 

# The function record_depend_distance is to record data from STM32  based on the distance detected by the ultrasonic sensor
def record_depend_distance(connectedPort,minDistance,maxDistance): 
	print("\n...Data is being transmitted from STM32...")
	s = serial.Serial(connectedPort,115200)
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
				#print(data.decode("utf-8").strip())
				distance = data.decode("utf-8").strip()
				#if distance is in the range call record to record voltage in CSV
				#distance = 9
				if distance < maxDistance and distance > minDistance:
					print("...Start recording...")
					# does computer need to send command to stm32 to read the ADC again to get votage 
					record(connectedPort) #recording to CSV 

				#out of range , stop recording
				else: 
					print("user is not in the given range")
					print("\n...stop recording...")
					print("...WAV file is being generated...")
					os.system("./c_processing_program/csv_to_wav python_interface_and_output_file/output.DATA python_interface_and_output_file/output.wav")
					s.close()
					break
			except UnicodeDecodeError:
				pass
	except KeyboardInterrupt:
		print("\n...stop recording...")
		s.close()
		
# The function send_to_uart is to sending data to STM32 via UART
def send_to_uart(command,connectedPort):
	try: 
		print("\n...Data is being sent to STM32...")
		ser = serial.Serial(connectedPort, 115200, timeout=10,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
		command = str(command)
		ser.write_timeout = 0
		ser.write(bytes(command,"utf-8"))

	except UnicodeDecodeError: 
		print("...errors with sending data...")
		pass



# def record_chosen_duration(connectedPort,audioDuration): 
# 	buff = ""
# 	data = []
# 	output = ""
# 	s = serial.Serial(connectedPort, baudrate=115200)
# 	'''
# 	while s.read(1) != b'\n':
# 		pass
# 	t = time.time()
# 	'''
# 	data = None
# 	while True:
# 		while data != b'\x00':
# 			data = s.read(1)
# 		data = s.read(7)
# 		data = s.read(4)
# 		if data == b'\x00\x00\x00\x00':
# 			break
# 	maxV = 0
