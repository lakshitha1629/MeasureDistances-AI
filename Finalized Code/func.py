import cv2
import numpy as np
import math
import cv2
from skimage.exposure import cumulative_distribution
import matplotlib.pylab as plt
import numpy as np

def cdf(im,template):
    '''
    computes the CDF of an image im as 2D numpy ndarray
    '''
    c, b = cumulative_distribution(im)
    c_t, b = cumulative_distribution(template)
    # pad the beginning and ending pixels and their CDF values
    c = np.insert(c, 0, [0]*b[0])
    c_t = np.insert(c_t, 0, [0] * b[0])
    c = np.append(c, [1]*(255-b[-1]))
    c_t = np.append(c_t, [1]*(255-b[-1]))
    return c,c_t

def hist_matching(c, c_t, im):
    '''
    c: CDF of input image computed with the function cdf()
    c_t: CDF of template image computed with the function cdf()
    im: input image as 2D numpy ndarray
    returns the modified pixel values
    '''
    pixels = np.arange(256)
    # find closest pixel-matches corresponding to the CDF of the input image, given the value of the CDF H of
    # the template image at the corresponding pixels, s.t. c_t = H(pixels) <=> pixels = H-1(c_t)
    new_pixels = np.interp(c, c_t, pixels)
    ims = (np.reshape(new_pixels[im.ravel()], im.shape)).astype(np.uint8)
    return ims



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

    # Find contours in thresh (find the rectangles).
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # [-2] indexing takes return value before last (due to OpenCV compatibility issues).
    font = cv2.FONT_HERSHEY_COMPLEX
    
    areaList = []
    outputList = []
            
    # Iterate rectangle contours
    for c in cnts:
        approx = cv2.approxPolyDP(c, 0.05*cv2.arcLength(c, True), True)
    #     cv2.drawContours(img, [approx], 0, (0), 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if (len(approx) == 4):  #  Ignore very small contours
            # Mark rectangle with green line
            cv2.drawContours(img, [approx], 0, (0, 255, 0), 1)
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(approx)
            ar = float(w)/h
            if (not(ar >= 0.95 and ar <= 1.05)) and ar>3:
                areaList.append(cv2.contourArea(approx))
                # Crop the bounding rectangle out of img
                out = img[y-10:y+h+10, x-10:x+w+10].copy()
                outputList.append(out)
                
    max_value = max(areaList)
    max_index = areaList.index(max_value)
    
    return outputList[max_index]
        


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

    print('point0 :',corners[0])
    print('point1 :', corners[1])
    print('point2 :', corners[2])
    print('point3 :', corners[3])
    
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

    length = (((x3)-(x4))**2 + ((y3)-(y4))**2)**0.5
    x = length
    # converting to float
    pyval = x.item()
    pyval = float(x)
    print('length :', length)
    pixelRatio =known_length/length

    print('Pixel_ratio: ', pixelRatio)

    return img , corners ,length, pixelRatio
