from pathlib import Path
from warpTools import four_point_transform
from cornerDetectionTools import find_corners
from rotationTools import rotate
import numpy as np
import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("inputpath", help = "input path to the directory with the image files with form <folder/etc>")
ap.add_argument("outputpath", help = "output path to the directory with the image files with form <folder/etc>")
ap.add_argument("-t", "--target_dimensions", type=list, help="Change the aspet ratio of image to conform to this")
ap.add_argument("-d", "--dilation", type=int, choices=range(0, 310), default=70, help="dilation value: how much to incease the wiggle room around the corners of the solar panel")


args = vars(ap.parse_args())
in_path = Path(args["inputpath"])
out_path = Path(args["outputpath"])
dl = args["dilation"]
target_dim = args["target_dimensions"]

if not target_dim:
    target_dim = (3994, 2213)

try:
	os.mkdir(out_path)
except:
	pass

faulty_images = []

for filename in os.listdir(in_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        filepath = str(in_path / filename)
        file_outpath = str(out_path / filename)
        print("warping:", filepath)
        image = cv2.imread(filepath)
        height, width, channels = image.shape
        corners = find_corners(image)
        if not corners:
            faulty_images.append(filepath)
            continue
        image = four_point_transform(image, corners)
        image = rotate(image)
        image = cv2.resize(image, target_dim)
        cv2.imwrite(file_outpath, image)

print("\nThe following images could not be processed:")
for filepath in faulty_images:
    print("\t", filepath)