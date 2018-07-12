import numpy as np
import cv2 as cv2
import os, errno
import random 
import skimage.io as io 
import scipy as sc
from skimage import data
from skimage.transform import rescale, resize
from skimage.util import random_noise
from skimage.color import rgb2gray
from PIL import Image

### Variables ###
inputPathMask =   'C:/Users/wohlfart/Desktop/masks_ID/masks'
outputPathMask = 'C:/Users/wohlfart/Desktop/masks_ID/'
id = 128
treshold = 128

### Functions ###

def traverseOverImageFolders(directoryOriginal):
    if os.path.exists(directoryOriginal):
        imagesOriginal = os.listdir(directoryOriginal)
        index = 0
        while index < len(imagesOriginal):
             
            img1 = io.imread(inputPathMask + '/' + imagesOriginal[index], True)
            arr = np.array(img1)
            arr[arr > treshold] = id
            Image.fromarray(arr).save(outputPathMask + '/' + imagesOriginal[index])
            
            index += 1
            if (index % 200 == 0): print (index)
    else:
        print ('The following path does not exists:',directoryOriginal)


### Calls ###
if (os.path.exists(inputPathMask)):
    
    #check for existing output path, if not make one
    if not os.path.exists(inputPathMask):
        try:
            os.makedirs(outputPathMask)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    traverseOverImageFolders(inputPathMask)

else:
    print ('The inputPath does not exist')