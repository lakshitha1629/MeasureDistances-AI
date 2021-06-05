#!/usr/bin/env python
# coding: utf-8

# In[6]:


import cv2
import numpy as np
import imutils

# Read input image
img = cv2.imread('ss.JPG')

# Convert from BGR to HSV color space
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Get the saturation plane - all black/white/gray pixels are zero, and colored pixels are above zero.
s = hsv[:, :, 1]

# detect yellow
lower_range = np.array([25, 50, 70])
upper_range = np.array([35, 255, 255])
mask = cv2.inRange(hsv, lower_range, upper_range)
cv2.imshow('mask', mask)

# Apply threshold on s - use automatic threshold algorithm (use THRESH_OTSU).
ret, thresh = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Find contours in thresh (find the triangles).
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # [-2] indexing takes return value before last (due to OpenCV compatibility issues).
font = cv2.FONT_HERSHEY_COMPLEX

# Iterate triangle contours
for c in cnts:
    approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c, True), True)
    cv2.drawContours(img, [approx], 0, (0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    
    if (cv2.contourArea(c) > 10) and (len(approx) == 5):  #  Ignore very small contours
        # Mark rectangle with blue line
        cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
        cv2.putText(img, "Rectangle", (x, y), font, 1, (0))
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(c)
        # Crop the bounding rectangle out of img
        out = img[y:y+h, x:x+w, :].copy()
        
cv2.imshow("shapes", img)
cv2.imshow("Crop", out)
cv2.waitKey(0)
cv2.destroyAllWindows()


# In[ ]:





# In[ ]:




