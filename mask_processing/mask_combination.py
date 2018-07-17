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
inputPathMask =   '/home/dan/Desktop/Datenset_Tower/parts/00/masks/data'
inputPathMask2 =   '/home/dan/Desktop/Datenset_Building2/parts/00/masks/data'
outputPathMask = '/home/dan/Desktop/Datenset_TowerBuilding/train/masks/data'

maskSize = (224,224)

id = 128
treshold = 128

### Functions ###

def mergeMask(maskList, filename):

    blank_image = np.zeros(maskSize, dtype=np.uint8)

    for x in range(maskList[0].shape[0]):
        for y in range(maskList[0].shape[1]):
            i = 0
            while i < len(maskList):
                #print(i)
                if (maskList[i][x,y] != 0):
                    blank_image[x,y] = maskList[i][x,y]
                i += 1
    #save the mask    
    Image.fromarray(blank_image).save(outputPathMask + '/' + filename)

def traverseOverImageFolders():

    if os.path.exists(inputPathMask):
        maskList1 = os.listdir(inputPathMask)
        maskList2 = os.listdir(inputPathMask2)

        index = 0
        while index < len(maskList1):

            mask1 = io.imread(inputPathMask + '/' + maskList1[index], True)
            mask1 = np.array(mask1)

            mask2 = io.imread(inputPathMask2 + '/' + maskList2[index], True)
            mask2 = np.array(mask2)

            maskList = list((mask1,mask2))

            if (maskList2[index] == maskList1[index]):
                mergeMask(maskList,maskList1[index])

            index += 1
            if (index % 200 == 0): print (index)
    else:
        print ('The following path does not exists:',inputPathMask)


### Calls ###
if (os.path.exists(inputPathMask)):

    #check for existing output path, if not make one
    if not os.path.exists(inputPathMask):
        try:
            os.makedirs(outputPathMask)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    traverseOverImageFolders()

else:
    print ('The inputPath does not exist')
