import cv2
import numpy as np
import jenkspy as jp
import math

def show(img, name="img"):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_slope(x1, y1, x2, y2):
    return (y2-y1)/(x2-x1)

def cluster_points(points, nclusters):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, _, centers = cv2.kmeans(points, nclusters, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
    return centers

def find_intersection(x1,y1,x2,y2,x3,y3,x4,y4):

        px= ( (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) ) 
        py= ( (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) )
        return px, py

def get_slopes(lines):
    slopes = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            slopes.append(get_slope(x1, y1, x2, y2))
    return slopes

def segment_lines(lines):
    all_positive = True
    slopes = get_slopes(lines)
    radian_slopes = []
    for slope in slopes:
        radian_slopes.append(math.atan(slope))
    min_s1, max_s1, max_s2, max_s3 = jp.jenks_breaks(radian_slopes, nb_class=3)
    lines1 = []
    lines2 = []
    lines3 = []
    h_slopes = []
    v_slopes = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            rad_slope = math.atan(get_slope(x1, y1, x2, y2))
            if rad_slope <= max_s1:
                lines1.append(line)
                v_slopes.append(rad_slope)
            elif rad_slope <= max_s2:
                lines2.append(line)
                h_slopes.append(rad_slope)
            else:
                lines3.append(line)
    
    counts = [[len(lines1), lines1], [len(lines2), lines2], [len(lines3), lines3]]
    print([c[0] for c in counts])
    try:
        m = counts.index(max(counts))
        v_lines = counts[m-1][1] + counts[m-2][1]
        h_lines = counts[m][1]
    except:
        lines1 = []
        lines2 =[]
        min_s1, max_s1, max_s2 = jp.jenks_breaks(radian_slopes, nb_class=2)
        for line in lines:
            for x1, y1, x2, y2 in line:
                rad_slope = math.atan(get_slope(x1, y1, x2, y2))
                if rad_slope <= max_s1:
                    lines1.append(line)
                    v_slopes.append(rad_slope)
                elif rad_slope <= max_s2:
                    lines2.append(line)
                    h_slopes.append(rad_slope)
                else:
                    lines3.append(line)
        h_lines = lines1
        v_lines = lines2
    return h_lines, v_lines


def i_line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return [A, B, -C]

def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False


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

def find_corners(img, dilation=60):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255-gray

    blur = cv2.blur(gray, (10, 10))
    ret,thresh = cv2.threshold(blur, 240, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((50,50), np.uint8) # Modify this for adjusting how much it can cover up holes
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    rect = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)

    edges = cv2.Canny(rect,50,150,apertureSize = 3)
    edges = cv2.dilate(edges, np.ones((10, 10), dtype=np.uint8))
    lines = cv2.HoughLinesP(edges,2,np.pi/360,100, 1, minLineLength=300,maxLineGap=600)

    h_lines, v_lines = segment_lines(lines)


    # Uncomment  code for debugging
    # houghimg = gray.copy()
    # for line in h_lines:
    #     for x1, y1, x2, y2 in line:
    #         color = np.random.randint(0,255,3).tolist()
    #         cv2.line(houghimg, (x1, y1), (x2, y2), color=(100, 100, 100), thickness=20)
    # for line in v_lines:
    #     for x1, y1, x2, y2 in line:
    #         color = np.random.randint(0,255,3).tolist()
    #         cv2.line(houghimg, (x1, y1), (x2, y2), color=(200, 200, 200), thickness=20)

    # find the line intersection points
    Px = []
    Py = []
    pts = []
    for h_line in h_lines:
        for v_line in v_lines:
            x1, y1, x2, y2 = h_line[0]
            x3, y3, x4, y4 = v_line[0]
            i_pt = find_intersection(float(x1), float(y1), float(x2), float(y2), float(x3), float(y3), float(x4), float(y4))
            if i_pt:
                Px.append(i_pt[0])
                Py.append(i_pt[1])

    
    # Uncomment code for debugging
    # intersectsimg = houghimg.copy()
    # for cx, cy in zip(Px, Py):
    #     cx = np.round(cx).astype(int)
    #     cy = np.round(cy).astype(int)
    #     color = np.random.randint(0,255,3).tolist() # random colors
    #     cv2.circle(intersectsimg, (cx, cy), radius=10, color=color, thickness=-1) # -1: filled circle

    P = np.float32(np.column_stack((Px, Py)))
    nclusters = 4
    centers = cluster_points(P, nclusters)

    # Uncomment code for debugging
    # for cx, cy in centers:
    #     cx = np.round(cx).astype(int)
    #     cy = np.round(cy).astype(int)
    #     cv2.circle(gray, (cx, cy), radius=10, color=[150, 150, 150], thickness=-1) # -1: filled circle
    # show(gray, "centers")
    centers = [[int(c[0]), int(c[1])] for c in centers]
    return centers
