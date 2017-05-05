import collections # for deque
import cv2
import numpy as np
import os.path
import Queue as Q
import glob
import color
import easygui
import shapedetection
import alphabet
import csv
pathSource = './filteredCropsMAIN/'

noNew = './noNew.JPG'
mycsv={
"path":None,
"shp":None,
"colorAlp":None,
"colorShp":None,
"alp":None}
header_written = False

def viewImages(imPath):
	for i,img in enumerate([os.path.join(imPath,fn) for fn in next(os.walk(imPath))[2]]):
		cv2.imshow("Image Verifier",cv2.imread(img))
		if cv2.waitKey(0)==27:
			cv2.destroyAllWindows()
			break
	if cv2.waitKey(0):
		cv2.destroyAllWindows()
	return
	    
def showSavePrev(d):	
	cv2.imshow("prevIm", cv2.resize(cv2.imread(pathSource+'crop_%s.JPG'%(d)),None, fx = .25, fy = .25))
		
	k = cv2.waitKey(0)
	if k == ord('y'): # (save current) or (save current and prev)
		# qq = save & move on ; qww = save, view previous,save prev
		color.colourAuto(imPath)
			
		shapedetection.find_squares(imPath)
			#cv2.destroyWindow("bin")
		cv2.destroyWindow("square")
			
	
	
	cv2.destroyWindow("prevIm")# do not remove destroyWindow() for "prevIm"!

def folderSize(path):
	num = len([f for f in os.listdir(path) 
			if os.path.isfile(os.path.join(path, f))])
	return num

def write_csv(mycsv):
    """ coroutine for writing dicts to a CSV as rows """
    global header_written
    # create a CSV writer object
    with open("fileinfo.csv", "a") as f:
        #while True:
        data = mycsv
        # don't bother writing anything unless we have GPS data
        print "data inside writer"
        print data
        if data['path']:
            print "hI"
            dw = csv.DictWriter(f, sorted(data.keys()))
            print "hI"
            if not header_written:
                dw.writeheader()
                header_written = True
            dw.writerow(data)

	
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
		imPath=pathSource+'crop_%s.JPG'%(d[i])
		mycsv['path']=imPath
		print imPath
		cv2.imshow("currentIm" , cv2.resize(cv2.imread(pathSource+'crop_%s.JPG'%(d[i])),None, fx = .25, fy = .25))
		k = cv2.waitKey(0)
		if k == ord('y'): # (save current) or (save current and prev)
			# qq = save & move on ; qww = save, view previous,save prev
			(colorAlpha,colorShape)=color.colourAuto(imPath)
			mycsv['colorAlp']=colorAlpha
			mycsv['colorShp']=colorShape
			print colorAlpha,colorShape
			shape=shapedetection.find_squares(imPath)
			mycsv['shp']=shape
			cv2.destroyWindow("square")
			print shape
			alpha=alphabet.alpmanual()
			mycsv['alp']=alpha
			#cv2.destroyWindow("bin")
			print mycsv
			#output = write_csv()
			#output.next()
			# pipe each GPS-data-containing dict from the generator to the CSV writer
			print("writing to CSV...")
			#[output.send(mycsv)]
			write_csv(mycsv) 	
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
