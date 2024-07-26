data = None
with open("output.csv", 'r') as f:
	data = f.read().strip().replace("\n", "").split(',')[:-1]
data = list(map(int, data))
newData = [None] * ((2 * len(data)) - 1)
newData[0] = data[0]
for i in range(1,len(data)):
	newData[(2*i)-1] = (data[i-1] + data[i]) // 2
	newData[2*i] = data[i]
newData = map(str, newData)
with open("output.csv", 'w') as f:
	f.write(",\n".join(newData))
