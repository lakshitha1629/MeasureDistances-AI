#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import func
import math
import imutils
from typing import Any


# In[2]:


def mouse_click(event, x, y, flags, param):
    #define the points array
    # to check if left mouse
    # button was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        #draw a circle
        cv2.circle(finalImg, (x,y),1,(0,0,255),2)
        #save the coordinates in points of array
        points.append((x,y))
        #connect with line
        if len(points) == 4:
            #imgR need to replaced as ims
            cv2.line(ims,points[0],points[1],(0,0,255),2)
            cv2.line(ims,points[2],points[3],(0,0,255),2)
            
            # font for left click event
            font = cv2.FONT_HERSHEY_SIMPLEX
            strXY =str(x) + ',' + str(y)
            #All the imgR replace as ims
            cv2.putText(ims, strXY, (x, y),font, 1, (255, 255, 0),2)
            cv2.imshow('finalImg', ims)
            [x1, y1] = points[0]
            [x2, y2] = points[1]
            [x3, y3] = points[2]
            [x4, y4] = points[3]
            lengthArc1 = math.sqrt((math.pow((x1 - x2),2) + math.pow((y1 - y2),2)))
            print('Saddle_Height: {}'.format(lengthArc1*pixelRatio))
            lengthArc2 = math.sqrt((math.pow((x3 - x4), 2) + math.pow((y3 - y4), 2)))
            print('Reach: {}'.format(lengthArc2 * pixelRatio))


# In[3]:


# Init
imagePath = 'w.jpg'
imgR = cv2.imread(imagePath)

# Create window with freedom of dimensions
cv2.namedWindow("finalImg",cv2.WINDOW_NORMAL)

# fetching the dimensions
wid = imgR.shape[1]
hgt = imgR.shape[0]
print("Image Size {}x{}".format(wid,hgt))

# Use camera resolution
# ims=cv2.resize(imgR ,(hgt,wid))
ims = cv2.imread('ss.JPG')


# Check conditions
mask = func.tag_detection(imgR)
# maskImg = cv2.imshow('mask',mask)

#ref image for calibration
##imgR need to be mask
img , corners ,length, pixelRatio = func.cameraCalibration(mask)

#applying the mouse event
finalImg = cv2.imshow('finalImg', ims)

points = []

cv2.setMouseCallback('finalImg', mouse_click)

cv2.waitKey(0)
cv2.destroyAllWindows() 


# In[ ]:





# In[ ]:




