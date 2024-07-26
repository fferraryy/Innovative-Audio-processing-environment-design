import numpy as np
import matplotlib.pyplot as plt
import csv

# Read data from csv
# data = np.loadtxt('project/output.csv', delimiter=',')
# print(data)

# dataList = []
# count = 0
# with open('project/output.csv', newline='') as csvfile:
#     	# Create a CSV reader object
# 		csvReader = csv.reader(csvfile)
		
#     	# Iterate over each row in the CSV file
# 		for row in csvReader:
#         # Each row is a list of values
# 			data = int(row[0])
# 			dataList.append(data)
# 			count = count + 1 


# # Set the number of points in 1 sec
# time_interval = 1 / 2500

# # Series of time
# time = np.arange(0, count * time_interval, time_interval)


# # Plotting
# plt.plot(time, dataList, 'o', color='b', markersize=2)
# plt.title('Voltage vs Time')
# plt.xlabel('Time (seconds)')
# plt.xticks(np.arange(0, count * time_interval + 1, 1))
# plt.ylabel('Voltage')
# plt.grid(True)
# plt.show()

# #save graph
# plt.savefig('Voltage_vs_time_plot.png')
dataList = []
with open('../project/moving_average_result.txt', 'r') as file:
	# Read lines from the text file
	lines = file.readlines()
			# Iterate over each line
	for line in lines:
     # Convert each line to an integer and add it to the dataList
		data = float(line.strip())
		dataList.append(data)

	# Calculate time interval
	time_interval = 1 / 2500
        # Create time array
	time = np.arange(0, len(dataList) * time_interval, time_interval)
        # Plotting
	plt.plot(time, dataList, '-', color='b', markersize=0.05)
	plt.title('Voltage vs Time')
	plt.xlabel('Time (s)')
	plt.ylabel('Voltage (V)')
	plt.grid(True)
        
 	# Save the plot
	plt.savefig("voltage_vs_time_plot.png")
        
        # Show the plot
	plt.show()
        
        # Close the plot window
	plt.close()
