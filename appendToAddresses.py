import sys

newLine = sys.argv[1]

with open("addresses.txt", "a") as myfile:
	myfile.write('\n' + newLine)

with open("addresses.txt") as f:
	text = f.readlines()
	size = len(text)

print (size-1)