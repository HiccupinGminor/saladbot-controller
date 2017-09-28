import cv2
import numpy as np
from matplotlib import pyplot as plt

def read_image(image_location):
    return cv2.imread(image_location)

def filter_green(img):
    hsv = cv2.cvtColor( img, cv2.COLOR_BGR2HSV)

    green_low = np.array([35,110,120])
    green_high = np.array([45,255,255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, green_low, green_high)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img,img, mask= mask)

    smoothed = cv2.blur(res,(20,20)) # Clear out small artefacts

    plt.imshow(smoothed)
    plt.show()

    # Is there a plant in image?
    h,s,v = cv2.split(smoothed)
    ret, v = cv2.threshold(v,100,255,cv2.THRESH_BINARY) # Filter out really faint (smoothed) images
    if (cv2.countNonZero(v) / v.size) > 0.001:
        return True
    return False
