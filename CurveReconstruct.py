from tkinter import *
from tkinter import ttk
import re
import os
import sys
sys.path.append("/tabs")
from tabs import FileTab, HelpTab, ToleranceTab, VersionTab, CrossEdge
filePath = ["..\\..\\Build\\apps\\ReconstructApp\\Debug\\ReconstructApp.exe"]
filePath.append("YourPathHere")
exePath = ""

def initialize():
    for i in filePath:
        if os.path.isfile(i):
            #print(i)
            global exePath 
            exePath = str(i)
            break

    fo = open("config.ini", "r")
    dictionary = {}
    for l in fo:
        if l[0] in ("}", "{", "#") or l == "\n":
            pass
        else:
            x = l.split(":")
            x[0] = re.findall(r'"([^"]*)"', x[0])
            x[1] = re.findall(r'"([^"]*)"', x[1])
            dictionary[x[0][0]] = x[1][0]

    fo.close()

    #File Select update

    displayDict = {k : dictionary.get(k) for k in \
        ("tangents", "edges", "circles", "centers", "outline", "deg3Circ")}

    optionsDict = {k : dictionary.get(k) for k in \
        ("scaleFactor", "amtRuns", "sparcity")}

    tolDict = {k : dictionary.get(k) for k in \
        ("point", "search", "initRadius", "worstDist", "ipEpsilon", "fitDist", \
        "fitAlpha","fitBeta","fitEpsilon", "angleEpsilon")}

    logDict = {k : dictionary.get(k) for k in \
        ("active", "maEdge", "markDirtyLog", "ptCloudIn", "maxEmpty")}

    debugDict = {k : dictionary.get(k) for k in \
        ("procSleep", "mst", "markDirty", "renderStep")}

    versDict = {k : dictionary.get(k) for k in \
        ("newFit", "nnVers" , "pruneUnfit", "triangle","localWorstDist", \
            "useFitness", "corCent", "edgeRepair")}

    fileSelTabObj.setSelected(eval(dictionary["fileSelect"]))
    fileSelTabObj.configMembers(optionsDict, displayDict)
    tolSelTab.configMembers(tolDict)
    verSelTab.configMembers(logDict, debugDict, versDict)
    crossTab.configMembers(dictionary)
    
    printCheckVal.set(eval(dictionary["print"]))
    clicked()
    clicked()
    changeImg()


def updateFile():
    fo = open("config.ini", "w")
    fo.write("{\n")
    fo.write("    \"quickstart\" : \"true\"\n\n")
    
    fileSelTabObj.printConfigOptions(fo)
    tolSelTab.printConfigOptions(fo)
    verSelTab.printConfigOptions(fo)
    
    fo.write("    \"print\" : \"" + str(printCheckVal.get()) + "\"\n\n")
    
    crossTab.printConfigOptions(fo)
    fo.write("}")
    fo.close()

def clicked():
    if printCheckVal.get() == 1:
        printCheckVal.set(False)
        printBTN.config(bg="red")
    else:    
        printCheckVal.set(True)
        printBTN.config(bg="green")

def run():
    updateFile()
    #print (exePath)
    if not (exePath == ""):
        print("test")
        x = os.spawnl(os.P_WAIT, str(exePath), " ")
        print(x, flush=True)

window = Tk()
window.geometry('1100x700+50+50')
window.resizable(False, False)
window.title("Curve Reconstruct Configuration Manager")
win1 = Frame(window, width = 600, height = 700)
win2 = Frame(window, width = 500, height = 700)
textOutputFrame = Frame(win2)
textWinScroll = Scrollbar(textOutputFrame)
textBox = Text(textOutputFrame)
textWinScroll.config(command=textBox.yview)
textBox.config(yscrollcommand=textWinScroll.set)
win1.pack(side='left', fill='y')
win2.pack(side='right', fill='x')

canvas = Canvas(win2, width=500, height=500)
canvas.pack(fill='x', expand=1)
textOutputFrame.pack(fill='both')
textWinScroll.pack(side='right', fill='y')
textBox.pack(side='left')
textString = "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat."
textBox.insert(END, textString)
img = [PhotoImage(file="img/tricaps.png")]
img.append(PhotoImage(file="img/octo.png"))
img.append(PhotoImage(file="img/bird.PNG"))
img.append(PhotoImage(file="img/bean.PNG"))
img.append(PhotoImage(file="img/beetle.PNG"))
img.append(PhotoImage(file="img/body.PNG"))
img.append(PhotoImage(file="img/maple.PNG"))
img.append(PhotoImage(file="img/giraffe.PNG"))
img.append(PhotoImage(file="img/m.PNG"))
img.append(PhotoImage(file="img/statue.PNG"))
img.append(PhotoImage(file="img/ring.PNG"))
img.append(PhotoImage(file="img/fork.PNG"))
img.append(PhotoImage(file="img/key.PNG"))
img.append(PhotoImage(file="img/lizzard.PNG"))
img.append(PhotoImage(file="img/rat.PNG"))
img.append(PhotoImage(file="img/device.PNG"))
img.append(PhotoImage(file="img/rectangles.PNG"))


#=================================================
#                    Tab Section
#=================================================
tab_control = ttk.Notebook(win1, width=600)

canvasImage = canvas.create_image(0, 0, anchor='nw', image=img[0])

def changeImg():
    canvas.itemconfig(canvasImage, image=img[fileSelTabObj.getSelected().get()-1])

fileSelTabObj = FileTab.FileSelectTab(tab_control, changeImg)
tolSelTab = ToleranceTab.ToleranceTab(tab_control)
verSelTab = VersionTab.VersionTab(tab_control)
helpTab = HelpTab.HelpFile(tab_control)
crossTab = CrossEdge.CrossEdgeTab(tab_control)
 
tab_control.add(fileSelTabObj, text='File Select')
tab_control.add(tolSelTab, text='Tolerance Select')
tab_control.add(verSelTab, text='Version Select')
tab_control.add(crossTab, text="Cross Edge Options")
tab_control.add(helpTab, text='Help Section')
 
printBTN = Button(win1, text="Print Results", font=('Helvetica', '24'), command= lambda: clicked(), bg="red")
updateBTN = Button(win1, text="Update Config", font=('Helvetica', '24'), command=updateFile, bg="#C0C0C0")
runBTN = Button(win1, text="Run Program", font=('Helvetica', '24'), command=run, bg="blue")

tab_control.pack(fill='both', expand=1)
updateBTN.pack(fill='x')
printBTN.pack(fill='x')
runBTN.pack(fill='x')

printCheckVal = BooleanVar()
printCheckVal.set(False)

initialize()
window.mainloop()
