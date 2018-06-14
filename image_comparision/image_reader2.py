import numpy as np
import cv2 as cv2
import os, errno
import image_processing as ip
import random 
import skimage.io as io 
from skimage import data
from skimage.transform import rescale, resize
from skimage.util import random_noise
from skimage.color import rgb2gray


### Variables ###
inputPathOriginal = 'C:/Users/wohlfart/Desktop/test_imagereader/Original'
inputPathMarked = 'C:/Users/wohlfart/Desktop/test_imagereader/Marked'

outputPathMask = 'C:/Users/wohlfart/Desktop/test_imagereader/masks'
outputPathOriginal = 'C:/Users/wohlfart/Desktop/test_imagereader/images'
markedColor = (255, 255, 255)

### Functions ###

def stop(): 
    img = cv2.imread('Example2_red.PNG',0)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

def saveAndProcessOriginalImage(img, imgPath):
    img = colorToGrayScaleImage(img)
    io.imsave(imgPath, img)

#Nach der Erstellung der Maske aufrufen 
def colorToGrayScaleImage(img):
    return rgb2gray(img)


def createDifferenceImage(img1, img2, newName):
    
    blank_image = np.zeros((img1.shape[0],img1.shape[1],3), np.uint8)

    #fill every difference with white pixel 
    for x in range(img1.shape[0]):
        for y in range(img1.shape[1]):
            if (img1[x,y] != img2[x,y]):
                blank_image[x,y] = markedColor

    
    #erosion to remove some noise
    blank_image = ip.erosionOnImage(blank_image)

    #save the mask
    io.imsave(outputPathMask + '/' + newName,blank_image)
   

def traverseOverImageFolders(directoryOriginal, directoryMarked):
    if os.path.exists(directoryOriginal):
        imagesOriginal = os.listdir(directoryOriginal)
        imagesMarked = os.listdir(directoryMarked)
        index = 0
        while index < len(imagesOriginal):
            img1 = io.imread(inputPathOriginal + '/' + imagesOriginal[index],1) 
            img2 = io.imread(inputPathMarked + '/' + imagesMarked[index],1)

            # preprocessing both images
            randAngle = random.randint(1,179)
            img1 = ip.rotateImage(img1,randAngle)
            img2 = ip.rotateImage(img2,randAngle)

            #create the mask 
            createDifferenceImage(img1, img2, imagesOriginal[index])
            
            #preprocessing the inputImage 
            saveAndProcessOriginalImage(img1, outputPathOriginal + '/' + imagesOriginal[index])
            
            index += 1
    else:
        print ('The following path does not exists:',directoryOriginal)





### Calls ###  
if (os.path.exists(inputPathOriginal)):
    
    #check for existing output path, if not make one
    if not os.path.exists(outputPathOriginal):
        try:
            os.makedirs(outputPathOriginal)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    traverseOverImageFolders(inputPathOriginal, inputPathMarked)

else:
    print ('The inputPath does not exist')