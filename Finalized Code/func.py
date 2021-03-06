import cv2
import numpy as np
import math

def screenCreate(image,camera_height=4608, camera_width=3456):
    # Create window with freedom of dimensions
    cv2.namedWindow("IMG",cv2.WINDOW_NORMAL)

    # Use camera resolution
    imS=cv2.resize(image,camera_height, camera_width)
#     fullImg =cv2.imshow('IMG' , imS)

    #return fullImg

def tag_detection(img):
    
    # Convert from BGR to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Get the saturation plane - all black/white/gray pixels are zero, and colored pixels are above zero.
    s = hsv[:, :, 1]

    # detect yellow
    lower_range = np.array([25, 50, 70])
    upper_range = np.array([35, 255, 255])
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # Apply threshold on s - use automatic threshold algorithm (use THRESH_OTSU).
    ret, thresh = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Find contours in thresh (find the triangles).
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # [-2] indexing takes return value before last (due to OpenCV compatibility issues).CHAIN_APPROX_NONE
    font = cv2.FONT_HERSHEY_COMPLEX

    # Iterate triangle contours
    for c in cnts:
        approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c, True), True)
#         cv2.drawContours(img, [approx], 0, (0), 3)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if (cv2.contourArea(c) > 10) and (len(approx) == 5):  #  Ignore very small contours
            x, y, w, h = cv2.boundingRect(c-10)
            # Crop the bounding rectangle out of img
            out = img[y:y+h+20, x:x+w+20].copy()
            return out


def cameraCalibration( img, known_length=50.0):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners =cv2.goodFeaturesToTrack(gray,4,0.01,10)
    corners =np.int0 (corners)

    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x,y),2 ,255, -1)

    pts1 = np.float32(corners)
    [[x1, y1]]= corners[0]
    [[x2, y2]] = corners[1]
    [[x3, y3]] = corners[2]
    [[x4, y4]] = corners[3]
    
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

    length = (((x2)-(x3))**2 + ((y2)-(y3))**2)**0.5
    x = length
    # converting to float
    pyval = x.item()
    print('length :', length)
    pixelRatio =known_length/length

    print('Pixel_ratio: ', pixelRatio)

    return img , corners ,length, pixelRatio
