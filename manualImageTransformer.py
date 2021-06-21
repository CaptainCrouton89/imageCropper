# **********************************************
# DEPRECATED
# **********************************************

# import the necessary packages
from warpTools import four_point_transform
import numpy as np
import argparse
import cv2
import os

def click_for_ref(event, x, y, flags, param):
	# grab references to the global variables
	global refPt
	if event == cv2.EVENT_LBUTTONUP:
		print('click number', len(refPt)+1)
		refPt.append([x, y])

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--inputpath", help = "input path to the directory with the image files with form <folder/etc/>")
ap.add_argument("-o", "--outputpath", help = "output path to the directory with the image files with form <folder/etc/>")
ap.add_argument("-t", "--templateimage", help = "name of the template image file. Should take form <name.png> or <name.jpg>")

args = vars(ap.parse_args())
in_path = args["inputpath"]
out_path = args["outputpath"]

try:
	os.mkdir(out_path)
except:
	pass

# Load template
image = cv2.imread(args["inputpath"] + args["templateimage"])
if np.shape(image) == (): # latest numpy / py3
	print("invalid image")
	exit(1)
clone = image.copy()
refPt = []

cv2.namedWindow("TemplateImage")
cv2.setMouseCallback("TemplateImage", click_for_ref)
cv2.imshow("TemplateImage", image)

# Gather reference points from template image
while True:
	print("Click the four corners of the solar panel, clockwise, \
			starting from the upper left.\
			\n\nPress 's' to save references, 'r' to reset them, or 'q' to abort.")
	while True:
		# display the image and wait for a keypress
		key = cv2.waitKey(1) & 0xFF
		# if the 'r' key is pressed, reset the cropping region
		if key == ord("r"):
			print("references reset")
			refPt = []
		elif key == ord("q"):
			exit(0)
		# if the 's' key is pressed, break from the loop
		elif key == ord("s"):
			cv2.destroyAllWindows()
			break
	# if there are two reference points, then crop the region of interest
	# from teh image and display it
	if len(refPt) == 4:
		print("Valid selection, warping image")
		break
	print("invalid selection, resetting points")
	refPt = []

cv2.destroyAllWindows()

warped = four_point_transform(image, refPt)

# show the original and warped images
cv2.imshow("Warped", warped)
print("Press 's' to save, or 'q' to abort.")
while True:
	# display the image and wait for a keypress
	key = cv2.waitKey(1) & 0xFF
	# if the 'r' key is pressed, reset the cropping region
	if key == ord("q"):
		exit(0)
	if key == ord("s"):
		print("saving references, performing warp on remaining images")
		break
cv2.destroyAllWindows()

# Transform remainining files
for filename in os.listdir(in_path):
	if filename.endswith(".jpg") or filename.endswith(".png"):
		print("warping:", os.path.join(in_path, filename))
		image = cv2.imread(in_path+filename)
		warped = four_point_transform(image, refPt)
		cv2.imwrite(out_path+filename, warped)

