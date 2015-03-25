from Tkinter import *
import tkFileDialog as tk
import tkMessageBox
import queue0

def filterForTargets():
	queue0.mainProcess()

def verifyFoldeImages():
	tkMessageBox.showinfo("Hello!", " Choose the image folder you want to view(only)!")
	pathToVerify = tk.askdirectory()
	queue0.viewImages(pathToVerify)
	return

windowA = Tk()
frameA = Frame(windowA)

folderAllImages = Button(frameA, text = "All images", command = filterForTargets).grid(row = 0, column= 0)
folderAlphanumeralTargets = Button(frameA, text = "Alpha-Numeral Targets", command = verifyFoldeImages).grid(row = 0, column= 1)
folderEmerging = Button(frameA, text = "Emergent", command=verifyFoldeImages ).grid(row = 0, column= 2)


labelFrameA = Label(windowA, text = "SYSTEM 0")
labelAllImages = Label(frameA, text = 'Click to filter out targets').grid(row=1, column=0)

labelFrameA.pack()
frameA.pack()
windowA.mainloop()
