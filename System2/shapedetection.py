import numpy as np
import cv2
from decimal import *
import easygui
import operator
def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
   # print "value"
   # print np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) )

    return ( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(imPath):
    img=cv2.imread(imPath)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    D={}
    for gray in cv2.split(img):
         for thrs in xrange(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
       
            
            #cv2.imshow('bin',bin)
            #cv2.waitKey(0)
            contours, hierarchy = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                #print "inside contour loop"
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                #print len(cnt)
                if len(cnt) ==3 and cv2.isContourConvex(cnt) and cv2.contourArea(cnt) > 500:
                    print "Triangle"

                    if D.has_key('triangle'):
                        D['triangle']+=1
                    # cg=cg+1
                    else :
                        D['triangle']=1
                    cv2.drawContours(img,[cnt],0,(0,255,0),2) 
                elif len(cnt) == 4 and cv2.contourArea(cnt) > 500 and cv2.isContourConvex(cnt): 
                    x,y,w,h=cv2.boundingRect(cnt)
                    print x,y,w,h
                 

                    #cnt = cnt.reshape(-1, 2)
                    # list1 = ([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    # max_cos=max(list1)
                    # min_cos=min(list1)
                    # print list1
                    # print max_cos,min_cos
                    # if max_cos <=0.3 and min_cos>=-0.1:
                        
                    #     print cnt
                    cv2.drawContours(img,[cnt],0,(0,255,0),2) 
                    
                    ratio=abs( 1-Decimal( w )/ h)
                    print ratio
                    if ratio<=0.02 :
                        print "square"
                        if D.has_key('square'):
                            D['square']+=1
                    # cg=cg+1
                        else :
                            D['square']=1
                    else:
                        print "rectangle"
                        if D.has_key('rectangle'):
                            D['rectangle']+=1
                    # cg=cg+1
                        else :
                            D['rectangle']=1
                elif len(cnt) == 5 and cv2.contourArea(cnt) > 500 and cv2.isContourConvex(cnt): 
                    cnt = cnt.reshape(-1, 2)
                    #print "Pentagon"
                    #cv2.drawContours(img,[cnt],0,(0,255,0),2) 
                    # list1 = ([angle_cos( cnt[i], cnt[(i+1) % 5], cnt[(i+2) % 5] ) for i in xrange(5)])
                    # max_cos=max(list1)
                    # min_cos=min(list1)
                    # print list1
                    # print max_cos,min_cos
                    # if max_cos <=-0.26 and min_cos>=-0.35:     
                    print "Pentagon"
                    if D.has_key('pentagon'):
                        D['pentagon']+=1
                    # cg=cg+1
                    else :
                        D['pentagon']=1
                    cv2.drawContours(img,[cnt],0,(0,255,0),2) 
                elif len(cnt) == 6 and cv2.contourArea(cnt) > 500 and cv2.isContourConvex(cnt): 
                    cnt = cnt.reshape(-1, 2)
                    # list1 = ([angle_cos( cnt[i], cnt[(i+1) % 6], cnt[(i+2) % 6] ) for i in xrange(6)])
                    # max_cos=max(list1)
                    # min_cos=min(list1)
                    # print list1
                    # print max_cos,min_cos
                    # if max_cos <=-0.45 and min_cos>=-0.55:   
                    print "Hexagon"
                    if D.has_key('hexagon'):
                        D['hexagon']+=1
                    # cg=cg+1
                    else :
                        D['hexagon']=1
                    cv2.drawContours(img,[cnt],0,(0,255,0),2)
                elif len(cnt) >9 and len(cnt)<=14 and cv2.contourArea(cnt)>500:
                    print "I am a star"
                    if D.has_key('star'):
                        D['star']+=1
                    # cg=cg+1
                    else :
                        D['star']=1
                    cv2.drawContours(img,[cnt],0,(0,255,0),2)
                elif len(cnt)>15 and cv2.contourArea(cnt) > 500 and cv2.isContourConvex(cnt): 
                    area=cv2.contourArea(cnt)
                    x,y,w,h = cv2.boundingRect(cnt)
                    radius=w/2
                    if abs(1-Decimal(w)/h)<=0.2 and abs(1-(area/3.1416*math.square(radius)))<=0.2:
                        print "circle"
                        if D.has_key('circle'):
                            D['circle']+=1
                    # cg=cg+1
                        else :
                            D['circle']=1
    
    
    sorted_D = sorted(D.items(), key=operator.itemgetter(1))

    print sorted_D
    shape= sorted_D[-1][0]
    print shape
    cv2.imshow('square', img)
    cv2.waitKey(0)
    z=easygui.ynbox('Shape Detection done', 'Title', ('Continue to alphabet', 'Go to manual'))
    print z
    if z==True:
        print "haha"

        
    else:
        print "---------------------Manual-------------------------"
        shape = easygui.enterbox(msg='What is the shape?', title=' Which SHAPE?', default='', strip=True)

        #shape = easygui.enterbox(msg='What is the the SHAPE?', title=' Which Shape?', default='', strip=True)
        print shape
    return shape


if __name__ == '__main__':

        img = cv2.imread('/home/sony/final/system3/crop3.jpg')
        find_squares(img)
 #       print squares
        # cv2.drawContours(img,squares,-1,(0,255,0),2) 
        #cv2.imshow('squares', img)
        #cv2.imshow('bin',bin)
        #cv2.waitKey(0)
