import serial
import sys
from serial_disk import getvalidPorts

port = None
if len(sys.argv) == 2:
	port = sys.argv[1]
else:
	ports = getvalidPorts()
	print("The available ports are:")
	for i,p in enumerate(ports):
		print(f"{i}. {p}")
	while True:
		portNum = input("please enter the number of the port you want to use: ")
		try:
			portNum = int(portNum)
			break
		except:
			print(f"invalid choice {portNum}. Please try again\n")
	port = ports[portNum]
	


s = serial.Serial(port, baudrate=115200)
try:
	while True:
		try:
			print(s.read(100).decode("utf-8"))
		except UnicodeDecodeError:
			print("failed to read data")
finally:
	s.close()

import serial
import sys
from serial_disk import getvalidPorts

SERIAL_PORT = '/dev/ttyUSB' # for mac only,'COM3' for windows
# cite: https://stackoverflow.com/questions/11784248/mac-os-analog-to-dev-ttyusbxx
BAUD_RATE = 115200

def parse_distance(line):
    if "Distance:" in line:
        parts = line.split()
        if len(parts) > 1:
            return parts[1]  # Assuming the format "Distance: VALUE cm"
    return None

def read_from_port(serial_connection):
    try:
        while True:
            if serial_connection.in_waiting > 0:
                reading = serial_connection.readline().decode('utf-8').strip()
                distance = parse_distance(reading)
                if distance:
                    print(f"Distance measured: {distance} cm")
                else:
                    print("Received data:", reading)
    except serial.SerialException:
        print("Error reading from the specified port.")
    except UnicodeDecodeError:
        print("Failed to decode incoming data.")
    except KeyboardInterrupt:
        print("Reading interrupted by the user.")

# Attempt to connect to the serial port
try:
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
        read_from_port(ser)
except serial.SerialException:
    print(f"Failed to connect on {SERIAL_PORT}.")
    print("Please check your port name and make sure the microcontroller is connected.")

       
