import numpy as np
import cv2
import webcolors1
import re
import operator
import glob
import os.path

filteredCropsPath = './filteredCropsMAIN/'

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors1.css3_hex_to_names.items():
	r_c, g_c, b_c = webcolors1.hex_to_rgb(key)
	rm = 0.5**( requested_colour[0] + r_c)
	#find distance b/w the 2 rgb values
	di = sum((2+rm, 4, 3-rm)*(requested_colour - webcolors1.hex_to_rgb(key))**2)**0.5	
	min_colours[(di)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors1.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def centroid_histogram(clt):
	# grab the number of different clusters and create a histogram
	# based on the number of pixels assigned to each cluster
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)
	#print clt.labels_
	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()

	# return the histogram
	return hist

def plot_colors(hist, centroids):
	# initialize the bar chart representing the relative frequency
	# of each of the colors
	l=[]
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0
	i=0;
	# loop over the percentage of each cluster and the color of
	# each cluster
	D={}
	cc=cblu=cbla=cg=cp=cpi=cgr=cr=cy=co=cbro=cw=cv=1 # initializing the number of clusters for each colour
	for (percent, color) in zip(hist, centroids):
		# plot the relative percentage of each cluster
		requested_colour = color
		actual_name, closest_name = get_colour_name(requested_colour)
		
		if re.search('cream.+', closest_name) :
			#print 'cream'
			l.append('cream')
			if D.has_key('cream'):
			 	D['cream']+=percent
			  # cc=cc+1
			else :
				D['cream']=percent

		elif re.search('blue.+', closest_name) :
		    #print 'blue'
		    l.append('blue')
		    if D.has_key('blue'):
				D['blue']+=percent
		        # cblu=cblu+1
		    else :
				D['blue']=percent

		elif re.search('green.+', closest_name) :
		    #print 'green'
		    l.append('green')
		    if D.has_key('green'):
				D['green']+=percent
			  # cg=cg+1
		    else :
				D['green']=percent

		elif re.search('red.+', closest_name) :
		    #print 'red'
		    l.append('red')
		    if D.has_key('red'):
				D['red']+=percent
			  # cr=cr+1
		    else :
				D['red']=percent

		elif re.search('yellow.+', closest_name) :
		    #print 'yellow'
		    l.append('yellow')
		    if D.has_key('yellow'):
				D['yellow']+=percent
			  # cy=cy+1
		    else :
				D['yellow']=percent

		elif re.search('purple.+', closest_name) :
		    #print 'purple'
		    l.append('purple')
		    if D.has_key('purple'):
				D['purple']+=percent
			  # cp = cp+1
		    else :
				D['purple']=percent

		elif re.search('gray.+', closest_name) :
		    #print 'gray'
		    l.append('gray')
		    if D.has_key('gray'):
				D['gray']+=percent
			  # cgr=cgr+1
		    else :
				D['gray']=percent

		elif re.search('brown.+', closest_name) :
		    #print 'brown'
		    l.append('brown')
		    if D.has_key('brown'):
				D['brown']+=percent
			  # cbro=cbro+1
		    else :
				D['brown']=percent

		elif re.search('orange.+', closest_name) :
		    #print 'orange'
		    l.append('orange')
		    if D.has_key('orange'):
				D['orange']+=percent
			  # co=co+1
		    else :
				D['orange']=percent

		elif re.search('pink.+', closest_name) :
		    #print 'pink'
		    l.append('pink')
		    if D.has_key('pink'):
				D['pink']+=percent
			  # cpi=cpi+1
		    else :
				D['pink']=percent

		elif re.search('white.+', closest_name) :
		    #print 'white'
		    l.append('white')
		    if D.has_key('white'):
				D['white']+=percent
			  # cw=cw+1
		    else :
				D['white']=percent

		elif re.search('violet.+', closest_name) :
		    #print 'violet'
		    l.append('violet')
		    if D.has_key('violet'):
				D['violet']+=percent
			  # cv=cv+1
		    else :
				D['violet']=percent

		elif re.search('black.+', closest_name) :
			#print 'black'
			l.append('black')
			if D.has_key('black'):
				D['black']+=percent
			  # cbla=cbla+1
			else :
				D['black']=percent

		else:
			#print closest_name
			l.append(closest_name)
			if D.has_key(closest_name):
				D[closest_name]+=percent
			else:
				D[closest_name]=percent
		
		endX = startX + (percent * 300)
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
			color.astype("uint8").tolist(), -1)
		startX = endX
	sorted_D = sorted(D.items(), key=operator.itemgetter(1))
	# maxRep = max(cc, cblu,cblu,cg,cp,cpi,cgr,cr,cy,co,cbro,cw,cv) #decides max times a class repeats in 5 clusters
	# print maxRep
	# # if ~(coloursFlag):
	# if maxRep == 3 or maxRep ==4: #for 5 clusters, only 3 colour classes exist 
	# 	# print "the color of the alphanumeric is %s"%(sorted_D[0][0])
	# 	# print "the color of the shape is %s"%(sorted_D[1][0])
	# 	alphaCol = sorted_D[0][0]
	# 	shapeCol = sorted_D[1][0]		
	# else:
	# 	try:
	# 		if (sorted_D[4][0]): #when all 5 cluster colours are distinct, there's a good possibility that the 2 colours(of shape & alphanumeral) are the 2nd and 3rd index
	# 			# print "the color of the alphanumeric is %s"%(sorted_D[2][0])
	# 			# print "the color of the shape is %s"%(sorted_D[3][0])
	# 			alphaCol = sorted_D[0][0]
	# 			shapeCol = sorted_D[1][0]
	# 	except IndexError:
	# 		# print "the color of the alphanumeric is %s"%(sorted_D[1][0])
	# 		# print "the color of the shape is %s"%(sorted_D[2][0])
	# 		alphaCol = sorted_D[0][0]
	# 		shapeCol = sorted_D[1][0]
	# 		print "%s"%(sorted_D)
	# # else:
	# 	# print 'exception!!!'
	# 	##experiment and figure it out
	return (bar, sorted_D,l[1],l[2])


