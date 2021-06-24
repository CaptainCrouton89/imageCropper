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

def get_slopes(lines):
    slopes = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            slopes.append(get_slope(x1, y1, x2, y2))
    return slopes

def cluster_points(points, nclusters):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, _, centers = cv2.kmeans(points, nclusters, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
    return centers

def find_intersection(x1,y1,x2,y2,x3,y3,x4,y4):

        px= ( (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) ) 
        py= ( (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) )
        return px, py

def segment_lines(lines):
    slopes = get_slopes(lines)
    radian_slopes = []
    for slope in slopes:
        radian_slopes.append(math.atan(slope))
    min_s1, max_s1, max_s2, max_s3, max_s4 = jp.jenks_breaks(radian_slopes, nb_class=4)
    lines1 = []
    lines2 = []
    lines3 = []
    lines4 = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            rad_slope = math.atan(get_slope(x1, y1, x2, y2))
            if rad_slope <= max_s1:
                lines1.append(line)
            elif rad_slope <= max_s2:
                lines2.append(line)
            elif rad_slope <= max_s3:
                lines3.append(line)
            elif rad_slope <= max_s4:
                lines4.append(line)
    return [lines1, lines2, lines3, lines4]

def get_intersections_of_linesets(lines1, lines2):
        Px = []
        Py = []
        for line1 in lines1:
            for line2 in lines2:                    
                x1, y1, x2, y2 = line1[0]
                x3, y3, x4, y4 = line2[0]
                i_pt = find_intersection(float(x1), float(y1), float(x2), float(y2), float(x3), float(y3), float(x4), float(y4))
                if i_pt:
                    Px.append(i_pt[0])
                    Py.append(i_pt[1])
        return Px, Py

def find_corners(img, dilation=60):
    height, width, channels = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255-gray

    blur = cv2.blur(gray, (10, 10))
    ret,thresh = cv2.threshold(blur, 240, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((50,50), np.uint8) # Modify this for adjusting how much it can cover up holes
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    rect = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)

    edges = cv2.Canny(rect,50,150,apertureSize = 3)
    edges = cv2.dilate(edges, np.ones((10, 10), dtype=np.uint8))
    lines = cv2.HoughLinesP(edges,2,np.pi/360,100, 1, minLineLength=1000,maxLineGap=200)

    all_lines = segment_lines(lines)

    # Uncomment  code for debugging
    # houghimg = gray.copy()
    # for i, line_set in enumerate(all_lines):
    #     for line in line_set:
    #         for x1, y1, x2, y2 in line:
    #             cv2.line(houghimg, (x1, y1), (x2, y2), color=(50*i, 50*i, 50*i), thickness=20)
    # show(houghimg, "lines")

    # find the line intersection points
    point_list = []
    point_list.append(get_intersections_of_linesets(all_lines[0], all_lines[1]))
    point_list.append(get_intersections_of_linesets(all_lines[0], all_lines[2]))
    point_list.append(get_intersections_of_linesets(all_lines[0], all_lines[3]))
    point_list.append(get_intersections_of_linesets(all_lines[1], all_lines[2]))
    point_list.append(get_intersections_of_linesets(all_lines[1], all_lines[3]))
    point_list.append(get_intersections_of_linesets(all_lines[2], all_lines[3]))

    Px = []
    Py = []
    for x_list, y_list in point_list:
        for x, y in zip(x_list, y_list):
            if x < 0 or x > width or y < 0 or y > height:
                continue
            else:
                Px.append(x)
                Py.append(y)

    # Uncomment code for debugging
    # intersectsimg = houghimg.copy()
    # for cx, cy in zip(Px, Py):
    #     cx = np.round(cx).astype(int)
    #     cy = np.round(cy).astype(int)
    #     color = np.random.randint(0,255,3).tolist()
    #     cv2.circle(intersectsimg, (cx, cy), radius=10, color=color, thickness=-1)
    # show(intersectsimg, "centers")

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
