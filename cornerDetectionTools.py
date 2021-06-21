import cv2
import numpy as np

def show(img, name="img"):
    cv2.imshow(name, img)
    cv2.waitKey(0)

def TL(l):
    max = np.inf
    pts = (0, 0)
    for x, y in l:
        if x+y < max:
            max = x+y
            pts = (x, y)
    return pts

def TR(l):
    max = -np.inf
    pts = (0, 0)
    for x, y in l:
        if x-y > max:
            max = x-y
            pts = (x, y)
    return pts

def BL(l):
    max = -np.inf
    pts = (0, 0)
    for x, y in l:
        if y-x > max:
            max = y-x
            pts = (x, y)
    return pts

def BR(l):
    max = -np.inf
    pts = (0, 0)
    for x, y in l:
        if x+y > max:
            max = x+y
            pts = (x, y)
    return pts

def find_corners(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255-gray

    blur = cv2.blur(gray, (10, 10))
    # do adaptive threshold on gray image
    ret,thresh = cv2.threshold(blur, 220, 255, cv2.THRESH_BINARY_INV)
    # apply morphology
    kernel = np.ones((40,40), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)
    # separate horizontal and vertical lines to filter out spots outside the rectangle
    kernel = np.ones((11, 5), np.uint8)
    vert = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((5,11), np.uint8)
    horiz = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

    # combine
    rect = cv2.add(horiz,vert)

    contours, hierarchy = cv2.findContours(rect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i, line in enumerate(contours):
        hull = cv2.convexHull(contours[i])
        cv2.drawContours(rect, [hull], 0, (100,100,100), 30)
        # Display the final convex hull image
    pts = []
    for point in hull:
        pts.append([point[0][0], point[0][1]])

    tl = TL(pts)
    tr = TR(pts)
    bl = BL(pts)
    br = BR(pts)
    return tl, tr, bl, br
