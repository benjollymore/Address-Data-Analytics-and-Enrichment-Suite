import json
import os
from subprocess import Popen
import webbrowser
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

print("Select a file for address data intake:")
processes = []
application_window = tk.Tk()
my_filetypes = [('all files', '.*'), ('text files', '.txt')]
# Ask the user to select a single file name.
controlFile = filedialog.askopenfilename(parent=application_window,
                                    initialdir=os.getcwd(),
                                    title="Please select file containing address dataset:",
                                    filetypes=my_filetypes)

print("File selected: " + controlFile)
print("Processing your request, please wait. When finished, a web interface will open.")

addresses = [line.rstrip('\n') for line in open(controlFile)]

#output = '{ "addresses":['

with open("codes.txt", 'w') as filetowrite:
    filetowrite.write('-')


for addr in addresses: 
	print("Processing: ", addr)
	command = 'python GeoLocations.py --ld --pad --pld --vj --sat --st --wp "' + addr + '" ' + str(addresses.index(addr)) +'  > JSON_FILES/' + str(addresses.index(addr)) + '.json'
	#print(command)
	processes.append(Popen(command, shell=True))

for p in processes: p.wait()


for j in range(0, len(addresses)):
	control = "JSON_FILES/" + str(j) + ".json"
	with open(control) as json_file:
		data = json.load(json_file)

		with open("codes.txt", "a") as myfile:
			if data['flags']['postOffice'] == "True":
				myfile.write('\n2')
			elif data['flags']['interesting'] == "True":
				myfile.write('\n1')
			else:
				myfile.write('\n0')

'''
for i in range(0, len(addresses)):
	control = str(i) + '.json'
	with open(control) as json_file:
		data = json.load(json_file)
	output += json.dumps(data)
	output += ", "
output = output[:-2]
output += " ]}"
outputJSON = json.loads(output)

with open('output.json', 'w') as outfile:
    json.dump(outputJSON, outfile)
'''
application_window.destroy()

print("Done!")
webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open("http://localhost")
