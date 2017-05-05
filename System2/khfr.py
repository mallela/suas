import numpy as np
import cv2
from decimal import *

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
   # print "value"
   # print np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) )

    return ( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    
    for gray in cv2.split(img):
       
            retval, bin = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            cv2.imshow('bin',bin)
            cv2.waitKey(0)
            contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                #print "inside contour loop"
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                #print len(cnt)
                if len(cnt) ==3 and cv2.isContourConvex(cnt) and cv2.contourArea(cnt) > 500:
                    print "Triangle"
                    cv2.drawContours(img,[cnt],0,(0,255,0),2) 
                elif len(cnt) == 4 and cv2.contourArea(cnt) > 500 and cv2.isContourConvex(cnt): 
                    x,y,w,h=cv2.boundingRect(cnt)
                    print x,y,w,h
                 

                    cnt = cnt.reshape(-1, 2)
                    list1 = ([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    max_cos=max(list1)
                    min_cos=min(list1)
                    print list1
                    print max_cos,min_cos
                    if max_cos <=0.3 and min_cos>=-0.1:
                        
                        print cnt
                        cv2.drawContours(img,[cnt],0,(0,255,0),2) 
                        
                        ratio=abs( 1-Decimal( w )/ h)
                        print ratio
                        if ratio<=0.02 :
                            print "square"
                        else:
                            print "rectangle"
                elif len(cnt) == 5 and cv2.contourArea(cnt) > 500 and cv2.isContourConvex(cnt): 
                    cnt = cnt.reshape(-1, 2)
                    #print "Pentagon"
                    #cv2.drawContours(img,[cnt],0,(0,255,0),2) 
                    list1 = ([angle_cos( cnt[i], cnt[(i+1) % 5], cnt[(i+2) % 5] ) for i in xrange(5)])
                    max_cos=max(list1)
                    min_cos=min(list1)
                    print list1
                    print max_cos,min_cos
                    if max_cos <=-0.26 and min_cos>=-0.35:     
                        print "Pentagon"
                        cv2.drawContours(img,[cnt],0,(0,255,0),2) 
                elif len(cnt) == 6 and cv2.contourArea(cnt) > 500 and cv2.isContourConvex(cnt): 
                    cnt = cnt.reshape(-1, 2)
                    list1 = ([angle_cos( cnt[i], cnt[(i+1) % 6], cnt[(i+2) % 6] ) for i in xrange(6)])
                    max_cos=max(list1)
                    min_cos=min(list1)
                    print list1
                    print max_cos,min_cos
                    if max_cos <=-0.45 and min_cos>=-0.55:   
                        print "Hexagon"
                        cv2.drawContours(img,[cnt],0,(0,255,0),2)
                elif len(cnt) >9 and len(cnt)<=14 and cv2.contourArea(cnt)>500:
                    print "I am a star"
                    cv2.drawContours(img,[cnt],0,(0,255,0),2)
                elif len(cnt)>15 and cv2.contourArea(cnt) > 500 and cv2.isContourConvex(cnt): 
                    area=cv2.contourArea(cnt)
                    x,y,w,h = cv2.boundingRect(cnt)
                    radius=w/2
                    if abs(1-Decimal(w)/h)<=0.2 and abs(1-(area/3.1416*math.square(radius)))<=0.2:
                        print "circle"
    
    

    cv2.imshow('result', img)
    cv2.waitKey(0)
    

if __name__ == '__main__':

        img = cv2.imread('/home/sony/DSC_0869cropped.JPG')
        find_squares(img)
 #       print squares
        # cv2.drawContours(img,squares,-1,(0,255,0),2) 
        #cv2.imshow('squares', img)
        #cv2.imshow('bin',bin)
        #cv2.waitKey(0)
