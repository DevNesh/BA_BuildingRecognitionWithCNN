import numpy as np
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
inputPathMask =  '/home/dan/Desktop/FINAL_DATASETS/Datenset_P/train/masks2/data'
outputPathMask = '/home/dan/Desktop/FINAL_DATASETS/Datenset_P/train/masks/data'
id = 255
treshold = 50

### Functions ###

def traverseOverImageFolders(directoryOriginal):
    if os.path.exists(directoryOriginal):
        imagesOriginal = os.listdir(directoryOriginal)
        index = 0
        while index < len(imagesOriginal):

            img1 = io.imread(inputPathMask + '/' + imagesOriginal[index], True)
            blank_image = np.zeros((224,224), dtype=np.uint8)
            blank_image[img1 > treshold] = id

            Image.fromarray(blank_image).save(outputPathMask + '/' + imagesOriginal[index])

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
