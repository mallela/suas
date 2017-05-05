import cv2
import numpy as np
import blob1
import Tkinter, Tkconstants, tkFileDialog
from Tkinter import *
from PIL import Image, ImageTk
import rot
import blob2

def backproject(path,info):
	im = cv2.imread(path)
	#im = cv2.resize(im, None, fx = 0.25, fy = 0.25)
	
	#image => hsv, hist
	hsv = cv2.cvtColor( im, cv2.COLOR_BGR2HSV)
	#cv2.imshow("hsv", hsv)
	imHist = cv2.calcHist([hsv], [0,1], None, [180, 256],[0,180,0,256])

	bckP = cv2.calcBackProject([hsv], [0,1], imHist,[0,180,0,256], 1)
	#cv2.imshow("bp", bckP)
	kernel = cv2.getStructuringElement( cv2.MORPH_ELLIPSE, (3,3))
	closing = cv2.morphologyEx(bckP, cv2.MORPH_CLOSE, kernel)
	#cv2.imshow("eroded", closing)

	##dst = cv2.filter2D(closing, -1,kernel)
	##cv2.imshow('2d', dst)

	ret,thresh = cv2.threshold(closing, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	#cv2.imshow("thresh", thresh)

	fm1 =  cv2.merge((thresh,thresh,thresh))
	res1 = cv2.bitwise_and(im, fm1, mask = None)# mask here has no significance
        #cv2.imshow("first and", res1)
	
	#make (lower bound) G= 180 for proper target. G= 90 makes its edges disappear a leeettle
	mask = cv2.inRange(hsv, np.array([5,90,50], dtype = np.uint8), np.array([49,255,205], dtype = np.uint8)) 
	mask_inv = cv2.bitwise_not(mask)
	res = cv2.bitwise_and(res1, res1, mask = mask_inv)
	#cv2.imwrite("final.jpg", res)
	kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
	res=cv2.erode(res,kernel,iterations=1)
	
    
	blob1.extractblob(res,info)
	#print "inside again"
	#rot.rota(res,info['direction'])
	#print "after"
if __name__ == '__main__':

	backproject("/home/sony/DSC_0897.JPG")
