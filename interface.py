from tkinter import *
from tkinter import ttk
#import GeoLocations.py

window = Tk()
window.geometry =('1100x700+50+50')
window.resizable(False, False)
window.title("Address information enchancement suite")

win1 = Frame(window, width=600, height=700)
win2 = Frame(window, width=500, height=700)

win1.pack(side='left', fill='y')
win2.pack(side='right', fill='x')

window.mainloop()