# The file serial_disk is to find and list available serial ports on the system

import serial
import serial.tools.list_ports

# Function getvalidPorts to find and return a list of valid serial ports
def getvalidPorts():
	validPort = []
	# iterate through all ports using
	ports = serial.tools.list_ports.comports()
	for port in ports: 
		try: 
		    #open each port 
		    ser = serial.Serial(port.device)
		    ser.close()
		    validPort.append(port.device)
		except (OSError, serial.SerialException): 
		    pass
	return validPort

if __name__ == "__main__":
	if len(getvalidPorts()) == 0:
		print("Could not find any valid ports")
	else:
		print("Found the following ports:")
		for port in getvalidPorts():
			print('-', port)


