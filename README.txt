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