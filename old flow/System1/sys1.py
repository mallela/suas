from Tkinter import *
import tkFileDialog as tk
import tkMessageBox
import queue1
import blobExtraction
import cv2
import numpy as np
import glob
import manualCrop

def filterImages():
	queue1.mainProcess()
	return

def verifyFoldeImages():
	tkMessageBox.showinfo("Hello!", " Choose the image folder you want to view(only)!")
	pathToVerify = tk.askdirectory()
	queue1.viewImages(pathToVerify)
	print pathToVerify
	return

def showImages():
	tkMessageBox.showinfo("Hello!", " Select your working directory with all alpha-numeral targets")
	pathToTargets= tk.askdirectory()
	x = glob.glob(pathToTargets+"/*.JPG")
	for i in range(0,len(x)):
		imPath = x[i]
		cv2.imshow("image" , cv2.resize(cv2.imread(imPath),None, fx = .25, fy = .25))
		k = cv2.waitKey(0)
		if k== ord('a'):
			blobExtraction.backproject(imPath)
		elif k==ord('x'):
			blobExtraction.edgeCase(imPath)
			#extractBlobs(imPath)
		elif k == ord('m'):
			manualCrop.manualCropProcess(imPath)
		elif k == 27:
			cv2.destroyAllWindows()
			break
		else:
			pass
	if cv2.waitKey(0):
		cv2.destroyAllWindows()
	return

if __name__=='__main__':
#def tkInterface():
	windowA = Tk()
	frameA = Frame(windowA)

	folderAlphanumeralTargets = Button(frameA, text = "Alpha-Numeral Targets", command = showImages).grid(row = 0, column= 0)
	folderSavedCrops = Button(frameA,text = "I'm full of crop", command = verifyFoldeImages).grid(row = 0, column= 1)
	folderFilteredBlobs = Button(frameA, text= "Filtered Crops", command = verifyFoldeImages).grid(row=0, column=2)
	clickToFilter = Button(frameA, text='Click to filter Crops', command=filterImages).grid(row=1, column=1)

	labelFrameA = Label(windowA, text = "SYSTEM 1").pack()
	labelAutoManual = Label(frameA, text = 'Press A for AUTO. \n Press M for MANUAL. \n Press X for EXCEPTION.').grid(row=1, column=0)
	labelDirectionsToEsc = Label(frameA, text = 'Press Esc to close').grid(row=2, column=1)
	frameA.pack()
	windowA.mainloop()