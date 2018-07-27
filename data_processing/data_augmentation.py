import numpy as np
import os, errno
import utils as ip
import random 
import skimage.io as io 
import scipy as sc
from scipy import misc
from skimage import data
from skimage.transform import rescale, resize
from skimage.util import random_noise
from skimage.color import rgb2gray
from PIL import Image

### Variables ###
inputPath = '/home/dan/Desktop/Datenset_Tower (Augmented)/validate/images/data'
imageSize = (224,224)   # size of outputimages

### Functions ###

def colorToGrayScaleImage(img):
    return rgb2gray(img)

def rotateImagesByRandomAngle(img1, img2):
    randAngle = random.randint(1,50)
    img1 = ip.rotateImage(img1,randAngle)
    img2 = ip.rotateImage(img2,randAngle)
    return (img1, img2)

def changeGammaOnImage(img1):
    randGamma = random.uniform(0.5,2)
    randGain = random.uniform(0.3,1)
    img1 = ip.gammaChangeImage(img1, randGamma, randGain)
    return img1

def changeGammaOnImages(img1, img2):
    randGamma = random.uniform(0.5,2)
    randGain = random.uniform(0.3,1)
    img1 = ip.gammaChangeImage(img1, randGamma, randGain)
    img2 = ip.gammaChangeImage(img2, randGamma, randGain)
    return (img1,img2)

def flipImagesHorizontal(img1, img2):
    return (ip.horizontalFlipImage(img1), ip.horizontalFlipImage(img2))

def preprocessingImages(img1, mask):

    resultImages = (img1, mask)
    #Random wie viele Funktionen aufgerufen werden
    iterations = random.randint(1,2)
    for i in range(0,iterations):
        randFunction = random.randint(0,3)
        #print ("** rand: ", randFunction)
        if randFunction == 0:
            resultImages = (changeGammaOnImage(resultImages[0]), mask)
        elif randFunction == 1:
            resultImages = flipImagesHorizontal(resultImages[0], resultImages[1])
        elif randFunction == 2:
            resultImages = rotateImagesByRandomAngle(resultImages[0], resultImages[1])
        elif randFunction == 3:
            resultImages = (ip.randomNoiseImage(resultImages[0]), mask)

    return resultImages

def traverseOverImageFolders():
    if os.path.exists(inputPath):
        images = os.listdir(inputPath)
        maskPath = inputPath.replace("images","masks")

        index = 0
        while index < len(images):

            # 50% if data augmentation should be used 
            if (random.randint(0,1) == 0):

                #read the images into a np array 
                image = io.imread(inputPath + '/' + images[index])
                mask = io.imread(maskPath + '/' + images[index], True)

                #preprocessing
                results = preprocessingImages(image, mask)

                #save the images
                io.imsave(inputPath + '/' + images[index], results[0])
                io.imsave(maskPath + '/' + images[index], results[1])
            
            index += 1
            if (index % 200 == 0): print (index)
    else:
        print ('The following path does not exists:',inputPath)


### Calls ###  
if (os.path.exists(inputPath)):
    traverseOverImageFolders()

else:
    print ('The inputPath does not exist')