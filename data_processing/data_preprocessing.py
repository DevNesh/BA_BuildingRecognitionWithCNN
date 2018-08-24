'''
Module, can be used for creating the ground truth images based on the taken
screenshots. 
'''
import numpy as np
import os, errno
import skimage.io as io 
import scipy as sc
from scipy import misc
from skimage import data
from skimage.transform import resize
from skimage.morphology import erosion, dilation
from PIL import Image

### Variables ###
inputPathOriginal = '/home/dan/Desktop/Datenset_skyscraper/parts/00/Original'
inputPathMarked =   '/home/dan/Desktop/Datenset_skyscraper/parts/00/Marked'

outputPathMask = '/home/dan/Desktop/Datenset_skyscraper/train/masks/data'
outputPathOriginal = '/home/dan/Desktop/Datenset_skyscraper/train/images/data'

markedColor = 255       # 8Bit / WHITE 
imageSize = (224,224)   # size of outputimages

### Functions ###

def createDifferenceImage(img1, img2, newName):
    '''
    Function, compares the given images pixelwise and creates a picture with the difference as a mask.
    Same pixel on the input images will be black, differences will be white on the new image. 
    '''    
    #create a new image
    blank_image = np.zeros(imageSize, dtype=np.uint8)

    #fill every difference with white pixel 
    for x in range(img1.shape[0]):
        for y in range(img1.shape[1]):
            if (img1[x,y] != img2[x,y]):
                blank_image[x,y] = markedColor

    #erosion + dilation to remove some noise
    blank_image = erosion(blank_image)
    blank_image = dilation(blank_image)

    #save the new mask    
    Image.fromarray(blank_image).save(outputPathMask + '/' + newName)


def traverseOverImageFolders(directoryOriginal, directoryMarked):
    ''' 
    Function, traverses over the given path, reads the normal image and the associated image with the
    marked object and creates the difference.
    '''
    if os.path.exists(directoryOriginal):
        imagesOriginal = os.listdir(directoryOriginal)
        imagesMarked = os.listdir(directoryMarked)
        index = 0
        while index < len(imagesOriginal):

            #read the images as grayscale into a np array 
            img1 = io.imread(inputPathOriginal + '/' + imagesOriginal[index], True)
            img2 = io.imread(inputPathMarked + '/' + imagesMarked[index], True)
            
            #rescale the images
            img1 = resize(img1, imageSize)            
            img2 = resize(img2, imageSize)
            images = (img1,img2)

            #create the mask 
            createDifferenceImage(images[0], images[1], imagesOriginal[index])
            
            #save the input image  
            io.imsave(outputPathOriginal + '/' + imagesOriginal[index], images[0])
            index += 1

            # info for progress
            if (index % 200 == 0): print (index)
    else:
        print ('The following path does not exists:',directoryOriginal)


### Calls ###  
if (os.path.exists(inputPathOriginal) and os.path.exists(inputPathMarked)):
    #check for existing output path, if not make one
    if not os.path.exists(outputPathOriginal):
        try:
            os.makedirs(outputPathOriginal)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    if not os.path.exists(outputPathMask):
        try:
            os.makedirs(outputPathMask)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    traverseOverImageFolders(inputPathOriginal, inputPathMarked)
else:
    print ('The inputPathOriginal or inputPathMarked does not exist')