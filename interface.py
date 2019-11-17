from tkinter import *
from tkinter import ttk
from PIL import Image
import sys
import os
import subprocess

query = ""
sys.argv = ['GeoLocations.py', '--ld', '--pld', '--wp', '--sat', '--pad', '--st', query, '> outfile.txt']
#import GeoLocations.py

window = Tk()
window.geometry =('1000x800+50+0')
window.resizable(False, False)
window.title("Address information enchancement suite")

mainWin = Frame(window, width=600, height=800)
'''
def changeImage():
	global satCanvas, strCanvas, satImg, strImg
	satImg = PhotoImage(file='satellite.png')
	image = Image.open('stView.jpg')
	image.save("stView.png")
	strImg = PhotoImage(file='stView.png')

	satCanvas.itemconfig(canvasImage, 
		image=satImg)
	strCanvas.itemconfig(canvasImage, 
	 	image=)

	satCanImg = satCanvas.create_image(0, 0, anchor='nw', image=satImg)
	strCanImg = strCanvas.create_image(0, 0, anchor='nw', image=strImg)
'''
def clicked():
	global labelText, v, query
	labelTest.config(text = v.get())
	query = v.get()
	print(query)
	qstr = 'python GeoLocations.py --ld --pld --wp --sat --pad --st "'
	endstr = '" > outfile.txt'
	run = qstr + query + endstr
	subprocess.run(run, shell=True)

spaceFrame = Frame(mainWin, height = 500)
v = StringVar()
submitButton = Button(mainWin, text='QUERY',
	font=('Helvetica', '24'), bg="green",
	command=lambda: clicked())
label = Label(mainWin, text="Address")

with open('outfile.txt', 'r', newline='') as content_file:
    content = content_file.read()

outVar = StringVar()
outVar.set(content)
outputBox = Entry(mainWin, textvariable=outVar, 
	state='readonly',width=100, wraplength=50)
e = Entry(mainWin, textvariable=v, width=100)
outputBox.pack(fill="both", side='top')
submitButton.pack(side='bottom', fill='x')
e.pack(side='bottom')
label.pack(side='bottom')
spaceFrame.pack(side='bottom')





imgContainers =Frame(window, width=400, height=800)
satImgWin = Frame(imgContainers, width=400, height=400)
strImgWin = Frame(imgContainers, width=400, height=400)

satCanvas = Canvas(satImgWin)
strCanvas = Canvas(strImgWin)

satCanvas.pack(fill='both')
strCanvas.pack(fill='both')

satImg = PhotoImage(file='satellite.png')
image = Image.open('stView.jpg')
image.save("stView.png")
strImg = PhotoImage(file='stView.png')

satImgWin.pack(fill='both')
strImgWin.pack(fill='both')

satCanImg = satCanvas.create_image(0, 0, anchor='nw', image=satImg)
strCanImg = strCanvas.create_image(0, 0, anchor='nw', image=strImg)

mainWin.pack(side='left')
imgContainers.pack(side='left')


window.mainloop()