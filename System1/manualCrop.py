import cv2
import cv2.cv as cv
from time import time
import queue1

boxes = []

cropsPath = '/home/praneeta/Desktop/Tkin/System1/allCrops1/'

def on_mouse(event, x, y, flags, params):
    # global img
    t = time()

    if event == cv.CV_EVENT_LBUTTONDOWN:
         print 'Start Mouse Position: '+str(x)+', '+str(y)
         sbox = [x, y]
         boxes.append(sbox)
    elif event == cv.CV_EVENT_LBUTTONUP:
        print 'End Mouse Position: '+str(x)+', '+str(y)
        ebox = [x, y]
        boxes.append(ebox)
        print boxes
        crop = img[boxes[-2][1]*4:boxes[-1][1]*4,boxes[-2][0]*4:boxes[-1][0]*4]
        cv2.imshow('crop',crop)
        k =  cv2.waitKey(0)
        if ord('q')==k:
            cv2.imwrite(cropsPath+'manualCrop_%d.JPG'%(queue1.folderSize(cropsPath)+1),crop)
            print cropsPath+'crop_%d.JPG'%(queue1.folderSize(cropsPath)+1)
            print "Written to file"

def manualCropProcess(imPath):
#if __name__ =='__main__':
    count = 0
    while(1):
        count += 1
        global img 
        img= cv2.imread(imPath,1)
        #img = cv2.resize(img, None, fx = 0.25,fy = 0.25)
        #height, width,_=img.shape
        cv2.namedWindow('real image')
        # cv2.resizeWindow('real image',int(width*.30),int(height*.30))
        cv.SetMouseCallback('real image', on_mouse, 0)
        imgRes = cv2.resize(img,None , fx = 0.25, fy = 0.25)
        cv2.imshow('real image', imgRes)
        if count < 50:
            if cv2.waitKey(33) == 27:
                cv2.destroyAllWindows()
                break
        elif count >= 50:
            if cv2.waitKey(0) == 27:
                cv2.destroyAllWindows()
                break
            count = 0
#manualCropProcess('/home/praneeta/Desktop/Tkin/System1/alphaNumeralTargets/DSC_0155.JPG')
