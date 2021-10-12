from pathlib import Path
from warpTools import four_point_transform
from cornerDetectionTools import find_corners
from rotationTools import rotate
import argparse
import cv2
import os
import time
from collections import defaultdict


ap = argparse.ArgumentParser()
ap.add_argument("inputpath", help = "input path to the directory with the image files with form <folder/etc>")
ap.add_argument("outputpath", help = "output path to the directory with the image files with form <folder/etc>")
ap.add_argument("-t", "--target_dimensions", type=tuple, help="Change the aspet ratio of image to conform to this")
ap.add_argument("-v", "--verbosity", type=int, default=1, help="Print intermediary steps")
ap.add_argument("-d", "--display", action="count", default=0, help="Display intermediary steps")
ap.add_argument("-s", "--timeit", default=False, help="Time image processing")
ap.add_argument("-r", "--rotate_override", default=0, type=int, help="Force rotate to 1=0° or 2=90°")

args = ap.parse_args()
in_path = Path(args.inputpath)
out_path = Path(args.outputpath)
target_dim = args.target_dimensions

if not target_dim:
    target_dim = (3994, 2213)

try:
	os.mkdir(out_path)
except:
	pass

faulty_images = []

print("Segmenting all images from", in_path)

start_time = time.time()
split = start_time
time_log = defaultdict(list)
def log_time(log="unlogged", msg=None):
    global start_time
    global split
    global time_log
    difference = time.time() - split
    if msg:
        print("\t\t\t\t", msg, "took", difference, "seconds")
    time_log[log].append(difference)
    split = time.time()

def print_runtime():
    global time_log
    print("\nTime Log:")
    for key, value in time_log.items():
        if key != "unlogged":
            avg = sum(value)/len(value)
            print("\tAverage {} time: \t{}".format(key, avg))

if args.timeit:
    log_time()
for filename in os.listdir(in_path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        filepath = str(in_path / filename)
        file_outpath = str(out_path / filename)
        if args.verbosity > 0:
            print("warping:", filepath)
        image = cv2.imread(filepath)
        height, width, channels = image.shape
        corners = find_corners(image, verbosity=args.verbosity, debug=args.display)
        if not corners:
            faulty_images.append(filepath)
            continue
        image = four_point_transform(image, corners, verbosity=args.verbosity, debug=args.display)
        if image.size == 0:
            faulty_images.append(filepath)
            continue
        image = rotate(image, verbosity=args.verbosity, debug=args.display)
        if image.size == 0:
            faulty_images.append(filepath)
            continue
        image = cv2.resize(image, target_dim)
        cv2.imwrite(file_outpath, image)
        if args.timeit:
            log_time("Full warp")

if args.timeit:
    print_runtime()

if faulty_images:
    if args.verbosity > 0:
        print("\nThe following images could not be processed:")
        for filepath in faulty_images:
            print("\t", filepath)