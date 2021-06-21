# import the necessary packages
from warpTools import four_point_transform
from cornerDetectionTools import find_corners
import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--inputpath", help = "input path to the directory with the image files with form <folder/etc/>")
ap.add_argument("-o", "--outputpath", help = "output path to the directory with the image files with form <folder/etc/>")

args = vars(ap.parse_args())
in_path = args["inputpath"]
out_path = args["outputpath"]

try:
	os.mkdir(out_path)
except:
	pass

# Transform remainining files
for filename in os.listdir(in_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        print("warping:", os.path.join(in_path, filename))
        image = cv2.imread(in_path+filename)
        tl, tr, bl, br = find_corners(image)
        warped = four_point_transform(image, [tl, tr, bl, br])
        cv2.imwrite(out_path+filename, warped)