import collections # for deque
import cv2
import numpy as np
import os.path
import Queue as Q
import glob
pathSource = '/home/praneeta/Desktop/Tkin/System1/allCrops1/'
pathDestination = '/home/praneeta/Desktop/Tkin/System1/filteredCrops2/'
noNew = '/home/praneeta/Desktop/Tkin/System1/noNew.JPG'

def viewImages(imPath):
	for i,img in enumerate([os.path.join(imPath,fn) for fn in next(os.walk(imPath))[2]]):
		cv2.imshow("Image Verifier", cv2.resize(cv2.imread(img),None, fx = .25, fy = .25)	)
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
	cv2.imshow("prevIm" , cv2.resize(cv2.imread(pathSource+'crop_%d.JPG'%(d)),None, fx = .25, fy = .25))
	l = cv2.waitKey(0)	
	if l == ord('w'): # previous save
		cv2.imwrite(pathDestination+'crop_%d.JPG'%(folderSize(pathDestination)+1), cv2.imread(pathSource+'crop_%d.JPG'%(d)))
	cv2.destroyWindow("prevIm")# do not remove destroyWindow() for "prevIm"!
	
def qDeq(x):
	q = Q.PriorityQueue()
	d = collections.deque()
	for i in x:
		dirName, fileName = os.path.split(i)
		shortName,_ = os.path.splitext(fileName)
		_,fir= shortName.split('_')
		print fir	
		q.put(int(fir))
	while not q.empty():
		d.append(q.get())
	print d
	return d

def slideShow(d, folderSizeBefore, sizFlag):
	if (sizFlag):
		x = folderSizeBefore # works over x = folderSizeBefore o.O idk why. Works in a strange way too. Starts looking at the folder last img first.
	else:
		x = 0
	for  i in range(x, len(d)):
		cv2.imshow("currentIm" , cv2.resize(cv2.imread(pathSource+'crop_%d.JPG'%(d[i])),None, fx = .25, fy = .25))
		k = cv2.waitKey(0)
		if k == ord('q'): # (save current) or (save current and prev)
			# qq = save & move on ; qww = save, view previous,save prev
			cv2.imwrite(pathDestination+'crop_%d.JPG'%(folderSize(pathDestination)+1), cv2.imread(pathSource+'crop_%d.JPG'%(d[i])))
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
			slideShow(d, folderSizeBefore, sizFlag)
			
		else :
			sizFlag = 0
			print "waiting..."
			k = cv2.waitKey(0)
			if k:
				cv2.imshow("currentIm", cv2.imread(noNew))
		if cv2.waitKey(0)==27:
			cv2.destroyAllWindows()
			break
	return
