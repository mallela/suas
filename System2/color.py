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



def colourAuto(imPath):

	image = cv2.imread(imPath)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# reshape the image to be a list of pixels
	image = image.reshape((image.shape[0] * image.shape[1], 3))

	# cluster the pixel intensities
	clt = KMeans(n_clusters = 5)
	clt.fit(image)

	# build a histogram of clusters and then create a figure representing the number of pixels labeled to each color
	hist = utils.centroid_histogram(clt)
	bar,sorted_D,colorAlpha,colorShape = utils.plot_colors(hist, clt.cluster_centers_)

		
	#cv2.imshow("bar",  cv2.cvtColor(bar, cv2.COLOR_BGR2RGB))
	print "RETURNED LIST - -------------------------------"
	print "color of the alphabet is %s"%(colorAlpha)
	print "color of the shape is %s"%(colorShape)
	z=easygui.ynbox('Color Detection done', 'Title', ('Continue with Shape', 'Go to manual'))
	print z
	if z==True:
				print "hello"
		
	else:
		(colorAlpha,colorShape) = colourManual()
		print "---------------------Manual-------------------------"
		print 'colour of alphanumeral is'+colorAlpha,'\ncolor of shape is'+colorShape #TODO write to .csv file inst
			
			
			
				
				
	return colorAlpha,colorShape



def colourManual():
	alphaColour = easygui.enterbox(msg='What is the colour of the ALPHANUMERAL?', title=' Which colour?', default='', strip=True)
	shapeColour = easygui.enterbox(msg='What is the colour of the SHAPE?', title=' Which colour?', default='', strip=True)
	#shape = easygui.enterbox(msg='What is the the SHAPE?', title=' Which Shape?', default='', strip=True)
	return alphaColour, shapeColour
