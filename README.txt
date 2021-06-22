****** For imageTransformer.py *********
This is a lightweight script using the opencv library for automatically warping all solar panel images in a directory into rectangular images.

To run the script, open terminal, and navigate to the folder in which this file is located. Then call this command (but with different options):

$ python imageTransformer.py input output

input: the input folder path
output: the output folder path

You may add the optional parameter -d <int> with any number between 0-300. This affects the dilation effect on the crop. The default is 60. If pieces of the image are getting cut off, increase this number. If too much is left over, decrease the number.

E.g:
$ python imageTransformer.py input output -d 10
$ python imageTransformer.py input output -d 90



****** For manualImageTransformer.py (deprecated) *********

This is a lightweight script using the opencv library for selecting a region of an image, warping it to a rectangular shape, and then applying that same warp to every other image in that image's directory.

To run the script, open terminal, and navigate to the folder in which this file is located. Then call this command (but with different options):

$ python imageTransformer.py -i preprocess/unedited/ -o preprocess/edited/ -t 0007_2021-04-13-09-38-35__LRP904033201201639218.jpg 

-i: the input folder of images to be processed
-o: the output folder of edited images
-t: the name of the template image you will use to warp the rest of the images. This image must also be in the input folder.

When clicking on corners of the image, start in the top left and work around clockwise: TL, TR, BR, BL


