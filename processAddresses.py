import json
import os
import subprocess
import webbrowser
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

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

output = '{ "addresses":['

for addr in addresses:
	print("Processing: ", addr)
	command = 'python helpers/GeoLocations.py --ld --pad --pld --vj --sat --st "' + addr + '" > ' + str(addresses.index(addr)) + '.json'
	subprocess.call(command, shell=True)

for i in range(0, len(addresses)):
	control = str(i) + '.json'
	with open(control) as json_file:
		data = json.load(json_file)
	output += json.dumps(data)
	output += ", "
output = output[:-2]
output += " ]}"
outputJSON = json.loads(output)
application_window.destroy()

print("Done!")
webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open("http://localhost")
