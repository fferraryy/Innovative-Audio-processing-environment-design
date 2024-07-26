import serial
import serial.tools.list_ports

validPort = []
#iterate through all ports using
ports = serial.tools.list_ports.comports()
for port in ports: 
    try: 
        #open each port 
        ser = serial.Serial(port.device)
        ser.close()
        validPort.append(port.device)
    except (OSError, serial.SerialException): 
        pass

if len(validPort) == 0:
	print("Could not find any valid ports")
else:
	print("Found the following ports:")
	for port in validPort:
		print('-', port)


