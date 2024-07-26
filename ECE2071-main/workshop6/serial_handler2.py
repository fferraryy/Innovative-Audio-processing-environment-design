import serial
import serial.tools.list_ports
from serial_disk import get_data
from serial_disk import findSTM32
from serial_disk import get_ports
from datetime import datetime
import time 


# foundPort = get_ports()
# connectedPort  = findSTM32(foundPort)

# #loop continuously runs if STM32 is connected and get the data from the STM32 
# ser = serial.Serial(connectedPort, 115200, timeout=10,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
# #while True: 
# ser.write_timeout = 0
# command = 'i'
# command = str(command)
# #ser.write(command.encode("utf-8"))
# ser.write(bytes('S',"utf-8"))
# print("sending\n")
        



        # try: 
        #     if connectedPort != 'None': 
                
                
        #         #data = get_data(connectedPort)[0]
        #         #print(data)
        #         print(connectedPort)
                 
        #         print("\n...Data is being sent to STM32...")
        #         ser = serial.Serial(connectedPort, 115200, timeout=10,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
        #         ser.write_timeout = 0
        #         ser.open()
        #         command = 'i'
        #         command = str(command)
        #         #ser.write(command.encode("utf-8"))
        #         #ser.write(bytes('S',"utf-8"))
        #         ser.write(chr(64))
        #         ser.close()
                

        #     else: 
        #         print("STM32 is not connected")
        #         break
        # except OSError: 
        #     print("STM32 is disconnected")
        #     break
        # except KeyboardInterrupt: 
        #     print("stop reading")
        #     break 



# Get the current datetime
# current_time = time.time()

# Print the current datetime

# audioDuration = 10
# startTime = time.time()
# print(startTime)
# timeDiff = 0 #initialise 
# while timeDiff < audioDuration:
# 	currentTime = time.time()
# 	print(currentTime)
# 	timeDiff = startTime - currentTime
# print(timeDiff)

# while True: 
	

import time

def time_difference(start_time):
    current_time = time.time()  # Get the current time in seconds since the epoch
    return current_time - start_time

# Record the start time
start_time = time.time()

# Use a while loop to continuously check the time difference
while True:
    diff = time_difference(start_time)
    print("Time difference:", diff, "seconds")
    
    if diff < 10:
        # If the time difference is less than 10 seconds, break out of the loop
        break
    
    time.sleep(1)  # Wait for 1 second before checking again