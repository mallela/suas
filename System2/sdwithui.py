import numpy as np
import cv2
import Tkinter, Tkconstants, tkFileDialog
from decimal import *
def shapedetect(filename):
	
	img = cv2.imread(filename)
	#gray = cv2.imread(filename,0)
	graycv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # whats the difference between this and the previous command ? 

	kernel = np.ones((5,5),np.uint8)
	erosion = cv2.erode(graycv,kernel,iterations = 1)
	binary=cv2.Canny(erosion,0,255)
	binary1=binary
	ret,thresh = cv2.threshold(binary,0,255,1)

	contours,h = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_L1)
	print len(contours)
	for cnt in contours:
		print "inside for loop"
		cv2.drawContours(img,[cnt],0,(0,255,0),3)
		approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
		print len(approx)

		if len(approx)==3:
			print "triangle"
			cv2.drawContours(img,[cnt],0,(0,255,0),3)
		elif len(approx)==4:
			cv2.drawContours(img,[cnt],0,(0,255,0),3)
			corners=len(approx)
			
			x,y,w,h=cv2.boundingRect(cnt)
			print x,y,w,h
			#box=cv2.cv.BoxPoints(rect)
			#box=np.int0(box)
			ratio=1 - Decimal( w )/ h
			print "ratio %d"%(ratio)



		elif len(approx)==5:
			print "pentagon"
			cv2.drawContours(img,[cnt],0,255,3)
			print "half-circle"
			cv2.drawContours(img,[cnt],0,(255,0,0),3)
		elif len(approx) == 11:
			print "star"
		elif len(approx) > 15:
			print "circle"
			cv2.drawContours(img,[cnt],0,(0,255,255),3)
	cv2.imshow('graycv', graycv)
	cv2.imshow('erode', erosion)
	cv2.imshow('binary',binary)
	cv2.imshow('img',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


if __name__=='__main__':
	shapedetect('/home/sony/System1/allCrops/crop_4.JPG')
 
