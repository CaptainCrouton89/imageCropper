import cv2
import numpy as np
import math
from cvTools import *

def _pre_process(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = 255-img
    img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,31,1) # cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,21,4
    show(img, "thresh")

    kernel = np.ones((4, 4), np.uint8) # Modify this for adjusting how much it can cover up holes
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=1)
    show(img, "open")


    # kernel = np.ones((2, 2), np.uint8) # Modify this for adjusting how much it can cover up holes
    # img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=1)
    # show(img, "close")

    # kernel = np.ones((3,3),np.float32)
    # img = cv2.filter2D(img,-1,kernel)
    # show(img)
    
    
    #img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=1)
    # show(img)
    # img = cv2.Canny(img,50,255,apertureSize = 5)
    # kernel = np.ones((20, 20), np.uint8) # 10 10 used to work for all but one
    # img = cv2.erode(img, kernel)
    # img = 255-img
    # show(img)
    return img

def rotate(img):
    processedimg = _pre_process(img.copy())

    h1 = img.copy()
    h2 = img.copy()
    h3 = img.copy()
    lines = cv2.HoughLinesP(processedimg,1,np.pi/2,1000, 1, minLineLength=800,maxLineGap=15)

    try:
        if lines == None:
            lines = cv2.HoughLinesP(processedimg,1,np.pi/360,1, 1, minLineLength=400,maxLineGap=30)
        try:
            if lines == None:
                print("No horizontal lines could be found to align perspective. Double check image for defects")
                return np.array([])
        except:
            pass
    except:
       pass
    

    # Uncomment for debugging
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(processedimg, (x1, y1), (x2, y2), color=(100, 100, 100), thickness=1)
    show(processedimg)

    slopes = get_slopes(lines)
    radian_slopes = [abs(math.atan(slope)) for slope in slopes]
    avg_slope = np.median(radian_slopes)
    # print("Average slope in radians:", avg_slope)

    if avg_slope > np.pi/4:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        print('rotated')
    return img

if __name__ == '__main__':
    path = "../data/warp_images/input/0100_2021-06-11-00-15-45.jpg"
    img = cv2.imread(path)
    img = rotate(img)
    show(img)