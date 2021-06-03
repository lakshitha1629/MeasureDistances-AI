import cv2
import numpy as np
import math

def cameraCalibration( img, known_length=50.0):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners =cv2.goodFeaturesToTrack(gray,4,0.01,10)
    corners =np.int0 (corners)

    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x,y),2 ,255, -1)
        #print(i)
    #cv2.imshow('corner', img)

    pts1 = np.float32(corners)
    #print(corners)
    [[x1, y1]]= corners[0]
    [[x2, y2]] = corners[1]
    [[x3, y3]] = corners[2]
    [[x4, y4]] = corners[3]
    print(corners[0])
    print(corners[1])
    print(corners[2])
    print(corners[3])
    font = cv2.FONT_HERSHEY_SIMPLEX
    #point1
    strXY = str(x1) + ',' + str(y1)
    cv2.putText(img, strXY, (x1, y1), font, 0.2, (255, 255, 0), 1)
    # point2
    strXY = str(x2) + ',' + str(y2)
    cv2.putText(img, strXY, (x2, y2), font, 0.2, (255, 255, 0), 1)
    # point3
    strXY = str(x3) + ',' + str(y3)
    cv2.putText(img, strXY, (x3, y3), font, 0.2, (255, 255, 0), 1)
    # point4
    strXY = str(x4) + ',' + str(y4)
    cv2.putText(img, strXY, (x4, y4), font, 0.2, (255, 255, 0), 1)


    cv2.imshow('RefImg', img)
    print('x2 :',x2,',','y2 :',y2)
    print('x3 :',x3, ',', 'y3:',y3)
    length = (((x2)-(x3))**2 + ((y2)-(y3))**2)**0.5
    x = length
    # converting to float
    print(type(x))
    pyval = x.item()
    print(type(pyval))
    print('length :', length)
    pixelRatio =known_length/length
    print(type( pixelRatio))
    print(type(pixelRatio.item()))

    print('Pixel_ratio: ', pixelRatio)

    return img , corners ,length, pixelRatio






