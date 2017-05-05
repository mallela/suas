import collections # for deque
import cv2
import numpy as np
import os.path
import Queue as Q
import glob
import os
import time
import easygui
from PIL import Image
# import PIL
from PIL.ExifTags import TAGS

pathSource = './allImagesMAIN/'
pathDestination = './targets1/'
pathEmergent = './emergent2/'
noNew = './noNew.JPG'

def saveToFolder(x,emergentOrTarget):
	with open(pathSource+'DSC_%s.JPG'%(x), 'rb') as f:
		data = f.read()
	if emergentOrTarget == 0:
		with open(pathDestination +'DSC_%s.JPG'%(x), 'wb') as f:
			f.write(data)
	else:
		with open(pathEmergent +'DSC_%s.JPG'%(x), 'wb') as f:
			f.write(data)

	return

def viewImages():
	for i,img in enumerate([os.path.join(imPath,fn) for fn in next(os.walk(imPath))[2]]):
		cv2.imshow("Image Verifier", cv2.resize(cv2.imread(img),None, fx = .25, fy = .25))
		if cv2.waitKey(0)==27:
			cv2.destroyAllWindows()
			break
	if cv2.waitKey(0):
		cv2.destroyAllWindows()
	return
	    
def folderSize(path):
	num = len([f for f in os.listdir(path) 
			if os.path.isfile(os.path.join(path, f))])
	return num

def showSavePrev(d):	
	cv2.imshow("prevIm", cv2.resize(cv2.imread(pathSource+'DSC_%s.JPG'%(d)),None, fx = .25, fy = .25))
	l = cv2.waitKey(0)	
	if l == ord('w'): # previous save
		# cv2.imwrite(pathDestination+'DSC_%s.JPG'%(folderSize(pathDestination)+1), cv2.imread(pathSource+'DSC_%s.JPG'%(d)))
		saveToFolder(d,0)
	elif l== ord('e'):
		# cv2.imwrite(pathEmergent+'DSC_%s.JPG'%(folderSize(pathEmergent)+1), cv2.imread(pathSource+'DSC_%s.JPG'%(d)))
		saveToFolder(d,1)
	cv2.destroyWindow("prevIm")# do not remove destroyWindow() for "prevIm"!
	
def qDeq(x):
	q = Q.PriorityQueue()
	d = collections.deque()
	for i in x:
		dirName, fileName = os.path.split(i)
		shortName,_ = os.path.splitext(fileName)
		_,fir= shortName.split('_')
		print fir	
		q.put((fir))
	while not q.empty():
		d.append(q.get())
	print d
	return d

def slideShow(d,folderSizeBefore, sizFlag):
	if (sizFlag):
		x = folderSizeBefore -1# works over x = folderSizeBefore o.O idk why. Works in a strange way too. Starts looking at the folder last img first.
	else:
		x = 0
	for i in range(x, len(d)):
		# blackHeader = cv2.copyMakeBorder(cv2.imread(pathSource+'DSC_%s.JPG'%(d[i])),200,0,0,0,cv2.BORDER_CONSTANT,value=(0,0,0))
		# cv2.putText(blackHeader, Image.open(pathSource+'DSC_%s.JPG'%(d[i]))._getexif()[36867], (150,150),cv2.FONT_HERSHEY_SIMPLEX, 4,(255,255,255),5)
		cv2.imshow("currentIm", cv2.resize(cv2.imread(pathSource+'DSC_%s.JPG'%(d[i])),None, fx = .25, fy = .25))
		k = cv2.waitKey(0)
		if k == ord('q'): # (save current) or (save current and prev)
			# qq = save & move on ; qww = save, view previous,save prev
			saveToFolder(d[i],0)
			# cv2.imwrite(pathDestination+'DSC_%s.JPG'%(folderSize(pathDestination)+1), cv2.imread(pathSource+'DSC_%s.JPG'%(d[i])))

			# sysPath = pathDestination+ 'DSC_%s.JPG'%((folderSize(pathDestination)+1)
			# time.sleep(2)
			# os.system('scp ./alphaNumeralTargets1/*.JPG sony@192.168.0.102:/home/sony/Transfer')
			# print 'adjbajyjfgju'
			m = cv2.waitKey(0)
			cv2.destroyWindow("currentIm")
			if m == ord('w'): 
				showSavePrev(d[i-1])
			else:
				pass
		elif k ==ord('e'):
			# cv2.imwrite(pathEmergent+'DSC_%s.JPG'%(folderSize(pathEmergent)+1), cv2.imread(pathSource+'DSC_%s.JPG'%(d[i])))
			saveToFolder(d[i],1)
			m = cv2.waitKey(0)
			cv2.destroyWindow("currentIm")
			if m == ord('w'): 
				showSavePrev(d[i-1])
			else:
				pass
		elif k == ord('w'): # ww = view previous, save previous
			showSavePrev(d[i-1])
		elif k== 27:
			cv2.destroyAllWindows()
			break
		else:
			pass
	return 0
	
#if __name__ == '__main__':
def mainProcess():

	siz = 0
	sizFlag = 0
	while True:
		x = glob.glob(pathSource+'*.JPG')
		print "size is%d"%(siz)
		if siz !=folderSize(pathSource):
			folderSizeBefore = siz
			siz = folderSize(pathSource)
			print "new size is%d"%(siz)
			sizFlag = 1		
			d = qDeq(x)
			updationMsgBox = easygui.msgbox("There has been an updation!", title = "Updates available")
			slideShow(d,folderSizeBefore, sizFlag)
			
		else :
			sizFlag = 0
			print "waiting..."
			# k = cv2.waitKey(0)
			if cv2.waitKey(0):
				cv2.imshow("currentIm", cv2.imread(noNew))
		if cv2.waitKey(0)==27:
			cv2.destroyAllWindows()
			break
	return