# **********************************************
# DEPRECATED
# **********************************************

from warpTools import four_point_transform
import numpy as np
import argparse
import cv2
import os

def click_for_ref(event, x, y, flags, param):
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

while True:
	print("Click the four corners of the solar panel, clockwise, \
			starting from the upper left.\
			\n\nPress 's' to save references, 'r' to reset them, or 'q' to abort.")
	while True:
		key = cv2.waitKey(1) & 0xFF
		if key == ord("r"):
			print("references reset")
			refPt = []
		elif key == ord("q"):
			exit(0)
		elif key == ord("s"):
			cv2.destroyAllWindows()
			break
	if len(refPt) == 4:
		print("Valid selection, warping image")
		break
	print("invalid selection, resetting points")
	refPt = []

cv2.destroyAllWindows()

warped = four_point_transform(image, refPt)

cv2.imshow("Warped", warped)
print("Press 's' to save, or 'q' to abort.")
while True:
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		exit(0)
	if key == ord("s"):
		print("saving references, performing warp on remaining images")
		break
cv2.destroyAllWindows()

for filename in os.listdir(in_path):
	if filename.endswith(".jpg") or filename.endswith(".png"):
		print("warping:", os.path.join(in_path, filename))
		image = cv2.imread(in_path+filename)
		warped = four_point_transform(image, refPt)
		cv2.imwrite(out_path+filename, warped)

