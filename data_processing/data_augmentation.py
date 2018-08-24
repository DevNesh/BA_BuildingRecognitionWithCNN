'''
Module, can be used to add data augmentation to the data.
'''
import numpy as np
import os, errno
import utils as ip
import random 
import skimage.io as io 
import scipy as sc
from scipy import misc
from skimage import data
from skimage.transform import resize, rotate
from skimage.util import random_noise
from skimage import exposure
from PIL import Image

### Variables ###
inputPath = '/home/dan/Desktop/Datenset_Block3/train/images/data'
imageSize = (224,224)   # size of outputimages

### Functions ###

def rotateImagesByRandomAngle(img1, img2):
    ''' 
    Function, rotates the given images in an random angle.
    Angle will be between 1 and 50.
    '''
    randAngle = random.randint(1,50)
    img1 = rotate(img1,randAngle)
    img2 = rotate(img2,randAngle)
    return (img1, img2)

def changeGammaOnImage(img1):
    '''
    Function, changes the gamma on the given image. Gamma will
    be changed by random values.
    '''
    randGamma = random.uniform(0.5,2)
    randGain = random.uniform(0.3,1)
    return exposure.adjust_gamma(img1, randGamma, randGain)

def flipImagesHorizontal(img1, img2):
    '''
    Function, flips the given images on the horizontal axis.
    '''
    return (img1[:, ::-1], img2[:, ::-1])

def preprocessingImages(img1, mask):
    '''
    Function, adds data augmentation on the given images. What kind of 
    augmentation will be used is decided randomly. Adds GammaChange, Rotation,
    Noise or flips the images.
    '''
    resultImages = (img1, mask)
   
    #choose randomly if two operations will be used 
    iterations = random.randint(1,2)

    # process the images
    for i in range(0,iterations):
        randFunction = random.randint(0,3)
        if randFunction == 0:
            resultImages = (changeGammaOnImage(resultImages[0]), resultImages[1])
        elif randFunction == 1:
            resultImages = flipImagesHorizontal(resultImages[0], resultImages[1])
        elif randFunction == 2:
            resultImages = rotateImagesByRandomAngle(resultImages[0], resultImages[1])
        elif randFunction == 3:
            resultImages = (random_noise(resultImages[0]), resultImages[1])

    return resultImages

def traverseOverImageFolders(path):
    ''' 
    Function, traverses over the given path, reads every image, takes every associated mask
    and adds a data augmentation on the half of the pictures.
    '''
    if os.path.exists(path):
        images = os.listdir(path)
        maskPath = path.replace("images","masks")
        
        if os.path.exists(maskPath):
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

                # info for progress
                if (index % 200 == 0): print (index)

        else:
            print ('The following path does not exists:',maskPath)
    else:
        print ('The following path does not exists:',path)


### Calls ###  
if (os.path.exists(inputPath)):
    traverseOverImageFolders(inputPath)

else:
    print ('The inputPath does not exist')