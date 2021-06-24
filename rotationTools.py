import cv2
import numpy as np
import math
from cvTools import *

def _pre_process(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = 255-img
    img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,21,4)
    kernel = np.ones((5,5), np.uint8) # Modify this for adjusting how much it can cover up holes
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=1)
    img = cv2.Canny(img,50,255,apertureSize = 5)
    kernel = np.ones((10,10), np.uint8)
    img = cv2.dilate(img, kernel)
    return img

def rotate(img):
    processedimg = _pre_process(img.copy())
    lines = cv2.HoughLinesP(processedimg,1,np.pi/90,1, 1, minLineLength=400,maxLineGap=10)

    # Uncomment for debugging
    # for line in lines:
    #     for x1, y1, x2, y2 in line:
    #         cv2.line(processedimg, (x1, y1), (x2, y2), color=(100, 100, 100), thickness=1)
    # show(processedimg)

    slopes = get_slopes(lines)
    radian_slopes = [math.atan(slope) for slope in slopes]

    avg_slope = np.median(radian_slopes)

    if avg_slope > 45 or avg_slope < -45:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    return img

if __name__ == '__main__':
    path = "../data/warp_images/input/0050_2021-06-10-02-46-50.jpg"
    img = cv2.imread(path)
    img = rotate(img)
    show(img)