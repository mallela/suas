import sys
import ntpath
import glob
from itertools import chain
from PIL.ExifTags import TAGS
from PIL import Image
import csv
from datetime import datetime as dt
import backproject1
import rot 
import cv2



def latlon(path):
    img=Image.open(path)
    info = img._getexif()
    #print info
    decoded = dict((TAGS.get(key, key), value) for key, value in info.items())
    info = {
       
        "lat": None,
        "lon": None,
       # "timestamp": None,
        "altitude": None,
        "direction":None
    }
   
    if not decoded.get('GPSInfo'):
        return info
    lat = [float(x) / float(y) for x, y in decoded['GPSInfo'][2]]
    lon = [float(x) / float(y) for x, y in decoded['GPSInfo'][4]]
    alt = float(decoded['GPSInfo'][6][0]) / float(decoded['GPSInfo'][6][1])
    direction=float(decoded['GPSInfo'][17][0])/float(decoded['GPSInfo'][17][1])
    
    
    info['lat'] = (lat[0] + lat[1] / 60)
    info['lon'] = (lon[0] + lon[1] / 60)
   
    info['altitude'] = alt
    info['direction']=direction
    if decoded['GPSInfo'][1] == "S":
        info['lat'] *= -1
    if decoded['GPSInfo'][3] == "W":
        info['lon'] *= -1
 
    if decoded['GPSInfo'][5] == 1:
        info['altitude'] *= -1
    info['altitude']=info['altitude']-860
    #print float(decoded['GPSInfo'][17][0])
    #print float(decoded['GPSInfo'][17][1])
    
    print info
    backproject1.backproject(path,info)
    rot.rota(path,-(info['direction']),info)
    return info



  


if __name__ == "__main__":
    path="/home/sony/junk1/alphaNumeralTargets1/DSC_9.JPG"
    image = Image.open(path)
    inf=latlon(path)
    print inf
    #r.rota(path,inf['direction'])
