# import the necessary packages
from pathlib import Path
from warpTools import four_point_transform
from cornerDetectionTools import find_corners
import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("inputpath", help = "input path to the directory with the image files with form <folder/etc>")
ap.add_argument("outputpath", help = "output path to the directory with the image files with form <folder/etc>")
ap.add_argument("-d", "--dilation", type=int, choices=range(0, 310), default=70, help="dilation value: how much to incease the wiggle room around the corners of the solar panel")

args = vars(ap.parse_args())
in_path = Path(args["inputpath"])
out_path = Path(args["outputpath"])
dl = args["dilation"]

try:
	os.mkdir(out_path)
except:
	pass

# Transform remainining files
for filename in os.listdir(in_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        filepath = str(in_path / filename)
        file_outpath = str(out_path / filename)
        print("warping:", filepath)
        image = cv2.imread(filepath)
        tl, tr, bl, br = find_corners(image, dl) # Change dilation value to adjust perimeter. 60 is default.
        warped = four_point_transform(image, [tl, tr, bl, br])
        cv2.imwrite(file_outpath, warped)