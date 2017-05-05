import cv2
import numpy as np
from decimal import *
import direction
import tkMessageBox
import rotpoint
import easygui
import rot
import math
def extractblob(im,info):
	
	print im.shape
	im1=im
	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imgray,0,255,0)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	#tkMessageBox.showinfo("Say Hello", "Hello World")
	easygui.msgbox("Press 'y' when you find the crop with the target", title="Verify")
	(h, w,d) = im.shape
	center = (w/2,h/2)
	print "center"
	print center
	z=0;
	for cnt in contours:
		if cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<10000:
			#print cv2.contourArea(cnt)
			cv2.drawContours(im,[cnt],0,(0,255,0),1)
			x,y,w,h = cv2.boundingRect(cnt)
			rect=cv2.minAreaRect(cnt)
			#print "x%d y%d  x1%d y1%d"%(x,y,x+w,y+h)
			#print "the center would be %d %d"%((x+x+w)/2,(y+y+h)/2)
			box=cv2.cv.BoxPoints(rect)
			box=np.int0(box)
			#print box
			#cv2.drawContours(im,[box],0,(0,0,255),2)
			cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,0),2)
			
			#print "w=%d h=%d x=%d y=%d"%(w,h,x,y)

			c=Decimal(rect[1][0])/Decimal(rect[1][1])
			d=Decimal(rect[1][1])/Decimal(rect[1][0])
			#print c
			#print d
			if c>Decimal(4)/Decimal(2) or d>Decimal(4)/Decimal(2):
				continue
			crop=im[y:y+h,x:x+w]
			
			
			#crop=cv2.medianBlur(crop,5)
			
			#cv2.rectangle(black_image,(x+w/2,y+h/2),(x+10+w/2,y+10+h/2),(0,255,0),3)
			#cv2.rectangle(im,(x+w/2,y+h/2),(x+10+w/2,y+10+h/2),(0,255,0),3)
			#print "ha"
			#x1=x+w/2
			#y1=y+h/2
			#black_image[y1,x1] = 255
			#print x+w/2,y+h/2
			
			#x,y=rotpoint.rotate(x+w/2,y+h/2,center,45)
			#rotpoint.changeref(center,x+w/2,y+h/2,im1)
			#cv2.rectangle(black_image,(x,y),(x+w,y+h),(0,255,0),3)
			
			cv2.imwrite("crop%d.jpg"%(z),crop)
			cv2.imshow("crop",crop);
			z=z+1;
			k = cv2.waitKey(0)
			if k == ord('y'):
				print "x and y of the crop"
				print x,y
				print "okay"
					# Press 't' if an image has a target in it
				print x+w/2,y+h/2
				#temp=(center[0]-(x+w/2))*(center[0]-(x+w/2)) + (center[1]-(y+h/2))*(center[1]-(y+h/2))
				#distimage=math.sqrt(temp)
				#print "length is %d"%(distimage)
				x,y=rotpoint.rotate(x+w/2,y+h/2,center,-info['direction'])
				#blobcentercoord=x+w/2,y+w/2
				rotpoint.changeref(center,x,y,im1,info)
				#rotatedcrop=rot.rota(crop,info['direction'])
				#direction.dir(crop,w,h)
				
				
			else:
				
				print "not okay"
				
		  
	cv2.destroyWindow("crop")		
	cv2.imwrite("windowtitled.JPG", im)
	#print '----------------------------------------'
	#list1=np.nonzero(black_image)
	#print list1
	#print "---------------------------------"
	#print np.count_nonzero(black_image)
	#print len(black_image)

	#cv2.line(black_image,(193,8),(922,675),(255),5)
	#cv2.line(black_image,(922,675),(2304,1536),(255),10)
	#cv2.line(black_image,(2304,1536),(193,8),(255),10)
	#print center
        #for i in range(0,np.count_nonzero(black_image)):
	#	cv2.line(black_image,center,(list1[0][i],list1[1][i]),(255),5)
	#	print list1[0][i]
	#	print list1[1][i]
	
	#cv2.imshow("hello",im)
	#cv2.imwrite("black.jpg",black_image)
	#cv2.waitKey(0)
	
