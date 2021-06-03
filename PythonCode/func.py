import cv2
import numpy as np
import math

def screenCreate(image,camera_height=4608, camera_width=3456):
    # Create window with freedom of dimensions
    cv2.namedWindow("IMG",cv2.WINDOW_NORMAL)

    # Use camera resolution
    imS=cv2.resize(image,camera_height, camera_width)
    fullImg =cv2.imshow('IMG' , imS)

    return fullImg

# this imS need to
def findColor(imgRN):

    hsv = cv2.cvtColor(imgRN, cv2.COLOR_BGR2HSV)

    lower_range = np.array([25, 50, 70])
    upper_range = np.array([35, 255, 255])

    mask = cv2.inRange(hsv, lower_range, upper_range)

    #cv2.imshow('image', img)
    cv2.imshow('mask', mask)

    return mask

def find_shapes(imgRN):
    font = cv2.FONT_HERSHEY_SIMPLEX

    imgGry = cv2.cvtColor(imgRN, cv2.COLOR_BGR2GRAY)

    ret, thrash = cv2.threshold(imgGry, 125, 125, cv2.CHAIN_APPROX_NONE)
    contours, hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        cv2.drawContours(imgRN, [approx], 0, (0, 0, 0), 1)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        if len(approx) == 3:
            cv2.putText(imgRN, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
        elif len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspectRatio = float(w) / h
#             print(aspectRatio)
            if aspectRatio >= 0.95 and aspectRatio < 1.05:
                cv2.putText(imgRN, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            else:
                print("Not square")
#                 cv2.putText(imgRN, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.2, (0, 0, 0))


#         elif len(approx) == 5:
#             cv2.putText(imgRN, "pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
#         elif len(approx) == 10:
#             cv2.putText(imgRN, "star", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
#         else:
#             cv2.putText(imgRN, "circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

    imgS =cv2.imshow('shapes', imgRN)

    return imgS



def region_of_interest(image):
    height = image.shape[0]
    mask = np.zeros_like(image, np.uint8)
    req_height = 0.4*height
    cv2.rectangle(mask, (0, int(req_height)), (int(image.shape[1]), int(height)), (0, 255, 0), 5)
    masked_image = cv2.bitwise_and(image, mask)
    f_image = cv2.bitwise_not(masked_image)

    return f_image

 #image = cv2.imread('image2.jpg')

 #copy_img = np.copy(image)
 #thresh_img = thresh(copy_img)
 #cropped_image = region_of_interest(thresh_img)

 #cv2.imshow('image', cropped_image)
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






