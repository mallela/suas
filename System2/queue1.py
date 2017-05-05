import collections # for deque
import cv2
import numpy as np
import os.path
import Queue as Q
import glob
import easygui
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import utils
import sdwithui

# global imagePath

pathSource = './filteredCropsMAIN/'
noNew = './noNew.JPG'

f = open('log2.txt','a')

def viewImages(imPath):
	for i,img in enumerate([os.path.join(imPath,fn) for fn in next(os.walk(imPath))[2]]):
		cv2.imshow("Image Verifier", cv2.imread(img))
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

def shapedetect(filename):
	sl =[]
	img = cv2.imread(filename)
	gray = cv2.imread(filename,0)
	graycv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # whats the difference between this and the previous command ? 

	kernel = np.ones((5,5),np.uint8)
	erosion = cv2.erode(gray,kernel,iterations = 1)

	ret,thresh = cv2.threshold(erosion,127,255,1)

	contours,h = cv2.findContours(thresh,1,2)
	#print len(contours)
	for cnt in contours:
	    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
	    #print len(approx)
	    if len(approx)==5:
	        #print "pentagon"
	        sl.append('pentagon')
	        cv2.drawContours(img,[cnt],0,255,-1)
	    elif len(approx)==3:
	        #print "triangle"
	        sl.append('triangle')
	        cv2.drawContours(img,[cnt],0,(0,255,0),-1)
	    elif len(approx)==4:
	        #print "square"
	        sl.append('square')
	        cv2.drawContours(img,[cnt],0,(0,0,255),-1)
	    elif len(approx) == 9:
	        #print "half-circle"
	        sl.append('half-circle')
	        cv2.drawContours(img,[cnt],0,(255,255,0),-1)
	    elif len(approx) == 11:
			#print "star"
			sl.append('star')
	    elif len(approx) > 15:
	        #print "circle"
	        sl.append('circle')
	        #cv2.drawContours(img,[cnt],0,(0,255,255),-1)
	#cv2.imshow('graycv', graycv)
	#cv2.imshow('erode', erosion)
	#cv2.imshow('gray',gray)
	#cv2.imshow('img',img)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	#print '---------------------------------------'
	#print sl
	try:
		if sl[1]:
			return sl[1]
		elif sl[0]:
			return sl[0]
		else:
			return 'not found'
	except:
		print 'not found'

def colourAuto(d, folderSizeBefore, sizFlag):
	typeoftarget='N/A'
	if (sizFlag):
		x = folderSizeBefore -1# works over x = folderSizeBefore o.O idk why. Works in a strange way too. Starts looking at the folder last img first.
	else:
		x = 0
	randomVariableName = easygui.msgbox("Press 'y' if you're satisfied with the output\n Press 'm' if it's a manual crop ", title = "Hello!")
	for  i in range(x, len(d)):
		# try:
		imagePath = pathSource+'crop_%d.JPG'%(d[i])
		imname = os.path.basename(imagePath)
		shape = shapedetect(imagePath)
		print "--------------Shape Detection Done-----------------------------" 
		print shape
		image = cv2.imread(imagePath,1)
		cv2.imshow("Colour?---------------", image)
		(bar, sorted_D,colorAlpha,colorShape) = colourAutoSubProcess(imagePath)
		#cv2.imshow("bar",  cv2.cvtColor(bar, cv2.COLOR_BGR2RGB))
		print "RETURNED LIST - -------------------------------"
		print colorAlpha, colorShape
		k = cv2.waitKey(0)
		if k== 27:
			cv2.destroyAllWindows()
			break
		else:
			#try:
				#colourChoiceALPHA = easygui.choicebox(msg= 'Which colour is the ALPHANUMERAL?', title= 'Colour?', choices=(sorted_D, 'None'))
				#colourChoiceSHAPE = easygui.choicebox(msg= 'Which colour is the SHAPE?', title= 'Colour?', choices=(sorted_D, 'None'))
				#shapeChoice = easygui.choicebox(msg= 'Which is the SHAPE?', title= 'Shape?', choices=(sorted_D, 'None'))
				#print 'colour of alphanumeral is'+colourChoiceALPHA,'\ncolor of shape is'+colourChoiceSHAPE #TODO write to .csv file instead
			#except TypeError:
			#	print 'colour of alphanumeral is N/A','\ncolor of shape is N/A'#TODO write to .csv file instead

			k2 = cv2.waitKey(0)
			if k2 == ord('m'):
				(colorAlpha,colorShape) = colourManual()
				try:
					print 'colour of alphanumeral is'+colorAlpha,'\ncolor of shape is'+colorShape #TODO write to .csv file inst
				except TypeError:
					print 'colour of alphanumeral is N/A','\ncolor of shape is N/A'#TODO write to .csv file instead

				if k2 == 27:
					cv2.destroyAllWindows()
					break
			if k2 == ord('s'):
				shape = shapeManual()
				print 'shape is '+shape
			if k2 == ord('a'):
				shape = shapeManual()
				(colorAlpha,colorShape) = colourManual()
				print 'colour of alphanumeral is'+colorAlpha,'\ncolor of shape is'+colorShape #TODO write to .csv file inst
				print 'shape is '+shape
		f.write('%d\t%s\t%s\t%s\t%s\t%s\n'%(i+2,imname,typeoftarget,shape,colorShape,colorAlpha))		
	return 0

def colourAutoSubProcess(imagePath):
	# load the image and convert it from BGR to RGB so that we can dispaly it with matplotlib
	image = cv2.imread(imagePath)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# reshape the image to be a list of pixels
	image = image.reshape((image.shape[0] * image.shape[1], 3))

	# cluster the pixel intensities
	clt = KMeans(n_clusters = 5)
	clt.fit(image)

	# build a histogram of clusters and then create a figure representing the number of pixels labeled to each color
	hist = utils.centroid_histogram(clt)
	#print clt.cluster_centers_
	bar,sorted_D,l1,l2 = utils.plot_colors(hist, clt.cluster_centers_)

	return (bar, sorted_D,l1,l2)

def colourManual():
	alphaColour = easygui.enterbox(msg='What is the colour of the ALPHANUMERAL?', title=' Which colour?', default='', strip=True)
	shapeColour = easygui.enterbox(msg='What is the colour of the SHAPE?', title=' Which colour?', default='', strip=True)
	#shape = easygui.enterbox(msg='What is the the SHAPE?', title=' Which Shape?', default='', strip=True)
	return alphaColour, shapeColour

def shapeManual():
	shape = easygui.enterbox(msg='What is the the SHAPE?', title=' Which Shape?', default='', strip=True)
	return shape

def alphabetDetectProcess(d, folderSizeBefore, sizFlag):
	if (sizFlag):
		x = folderSizeBefore -1# works over x = folderSizeBefore o.O idk why. Works in a strange way too. Starts looking at the folder last img first.
	else:
		x = 0
	for  i in range(x, len(d)):
		imagePath = pathSource+'crop_%d.JPG'%(d[i])
		cv2.imshow("alphabet?", cv2.imread(imagePath))
		cv2.waitKey(0)
		alphaNumeral = easygui.enterbox(msg='Enter the Alphanumeral.', title=' Which letter?', default='', strip=True)
		print alphaNumeral, 'crop_%d.JPG'%(d[i])
		
		if cv2.waitKey(0)==27:
			cv2.destroyAllWindows()
			break
	
	return

#if __name__ == '__main__':
def mainProcess(processFlag):
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
			if processFlag==1:
				colourAuto(d, folderSizeBefore, sizFlag)
			elif processFlag==2:
				alphabetDetectProcess(d,folderSizeBefore, sizFlag)
			else:
				print 111234567890
			
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
