from typing import Any

import cv2
import numpy as np
import func
import math

refPath = 'refImage.jpg'
imagePath2 = 'sample.jpg'
print(type(imagePath2))
# <class 'numpy.ndarray'>

print(imagePath2)
print(type(imagePath2))


# Create window with freedom of dimensions
cv2.namedWindow("finalImg",cv2.WINDOW_NORMAL)
imgR = cv2.imread(imagePath2)
img = cv2.imread(refPath)
# Use camera resolution
ims=cv2.resize(imgR ,(3264,2448))
cv2.imshow("finalImg" , ims)


#imagePath ='fullIlmg.jpg'
#image =cv2.imread('imagePath')

#fullImg =func.screenCreate(image,4608,3456)


imgRN = cv2.imread('sample_1.jpg')

mask = func.findColor(imgRN)
imgS = func.find_shapes(imgRN)
#ref image for calibration
img , corners ,length, pixelRatio =func.cameraCalibration(img)

#applying the mouse event

finalImg = cv2.imshow('finalImg',ims)

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
          cv2.line(imgR,points[0],points[1],(0,0,255),2)
          cv2.line(imgR,points[2],points[3],(0,0,255),2)
         #font for left click event
        print(x, ',',y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY =str(x) + ',' + str(y)
        #All the imgR replace as ims
        cv2.putText(imgR, strXY, (x, y),font, 1, (255, 255, 0),2)
        cv2.imshow('finalImg', imgR)
        [x1, y1] = points[0]
        [x2, y2] = points[1]
        [x3, y3] = points[2]
        [x4, y4] = points[3]
        print(points[0])
        print(points[1])
        print(points[2])
        print(points[3])
        print('x1 :', x1, ',', 'y1 :', y1)
        print('x2 :', x2, ',', 'y2 :', y2)
        print('x3 :', x3, ',', 'y3 :', y3)
        print('x4 :', x4, ',', 'y4 :', y4)
        lengthArc1 = math.sqrt((math.pow((x1 - x2),2) + math.pow((y1 - y2),2)))
        print('Pixel ratio:',pixelRatio )
        print('Saddle_Height:',(lengthArc1*pixelRatio))
        lengthArc2 = math.sqrt((math.pow((x3 - x4), 2) + math.pow((y3 - y4), 2)))
        print('Pixel ratio:', pixelRatio)
        print('Reach:', (lengthArc2 * pixelRatio))


       #print(type(lengthArc.item()))

points = []

cv2.setMouseCallback('finalImg', mouse_click)




cv2.waitKey(0)
cv2.destroyAllWindows() 

