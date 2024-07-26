import serial
import serial.tools.list_ports

def getvalidPorts():
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
	return validPort


#function to seach for available ports, return name of the ports 
def get_ports(): 
    ports = serial.tools.list_ports.comports()
    return ports

#function to find the connection with STM32, take all available ports and find which one is connected to STM32
#retunr port connected to STM32 
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

#function to read data/signal recieved from STM32 
def get_data(connectedPort): 
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
			except UnicodeDecodeError:
				pass
	except KeyboardInterrupt:
		print("\nClosing port")
		s.close()


foundPort = get_ports()
connectedPort  = findSTM32(foundPort)


if __name__ == "__main__":
	if len(getvalidPorts()) == 0:
		print("Could not find any valid ports")
	else:
		print("Found the following ports:")
		for port in getvalidPorts():
			print('-', port)


