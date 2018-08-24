'''
Module, defines functions for pre- and postprocessing the data for the 
neural network. Contains mask operations and data loader functionality.     
'''

import keras.backend as K
from keras import metrics
from keras.losses import *
from keras.preprocessing.image import ImageDataGenerator
import skimage.io as io
import skimage.transform as tr
import skimage.color
from skimage import img_as_ubyte
import numpy as np
from glob import glob
import os, errno
from PIL import Image


### Mask Operations ###

def fix_mask(mask, threshold = 100):
    '''
    Sets all pixel to 0 or 255 depending on the threshold.
    '''
    mask[mask < threshold] = 0.0
    mask[mask >= threshold] = 255.0
    return mask


def compareMasks(prediction, groundTruth):
    '''
    Compares two masks. A prediction and a ground-truth. Returns an image where:
    white pixel = true positives
    black pixel = true negative
    red pixel = false negative
    green pixel = false positive
    '''
    diff_img = np.zeros((224,224,3), dtype=np.uint8)

    for x in range(prediction.shape[0]):
        for y in range(prediction.shape[1]):
            if ((prediction[x,y] == groundTruth[x,y]) & groundTruth[x,y].all() != False):
                diff_img[x,y] = (255,255,255)
            elif (prediction[x,y] > groundTruth[x,y]):
                diff_img[x,y] = (255,0,0)
            elif (groundTruth[x,y] > prediction[x,y]):
                diff_img[x,y] = (0,255,0)

    return diff_img  


def setPixelToID(mask, id, threshold):
    '''
    Sets all pixel that are bigger than the defined threshold to the 
    given id and returns the image.
    '''
    mask[mask > threshold] = id
    return mask


def mergeMask(maskList, filename):
    '''
    Gets a list of masks and writes the values for each mask
    on a new image, so that the new image has the values of 
    each mask. 
    '''
    xSize = maskList[0].shape[0] 
    ySize = maskList[0].shape[1]

    result = np.zeros((xSize,ySize), dtype=np.uint8)
    i = 0

    for i in range (len(maskList)):
        for x in range(xSize):
            for y in range(ySize):
                if (maskList[i][x,y] != 0):
                    result[x,y] = maskList[i][x,y]
    
    return result


def postProcessMask(mask, threshold = 0.3):
    '''
    Setting the predicted propabilities to pixel the values 
    black or white, depending on the threshold.  
    '''
    mask[mask > threshold] = 255
    mask[mask <= threshold] = 0
    return mask

### Image Preparation for Neural Network  ###

def adjustData(img,mask):
    '''
    Maps the pixel values to a range from 0 to 1 for
    the given images and returns both images.
    '''
    mask = fix_mask(mask, 100)
    img = img/255.
    mask = mask/255.
    return (img,mask)


def loadData(inputPath, outputPath, bs = 32, save_dir=None):
    '''
    Creates the Keras defined ImageDataGenerators for processing a
    huge amount of data. 
    '''
    image_generator = ImageDataGenerator().flow_from_directory(inputPath, color_mode ='grayscale', target_size=(224,224), batch_size=bs, class_mode=None, save_to_dir = save_dir, shuffle=False,seed=1)
    mask_generator =  ImageDataGenerator().flow_from_directory(outputPath,  color_mode ='grayscale', target_size=(224,224), batch_size=bs, class_mode=None, save_to_dir = save_dir,shuffle=False, seed=1)

    train_generator = zip(image_generator, mask_generator)

    for (img,mask) in train_generator:
        img,mask = adjustData(img,mask)
        yield (img,mask)


def read_img(path, size):
    '''
    Reading an image from the given path and resizes the image
    to the given size. Returns the image. 
    '''
    img = io.imread(path)
    img = tr.resize(img, size)
    img_as_ubyte(img)
    return img


def read_imgs(path, size):
    '''
    Reading all images from the given path and resizes them to 
    the given size. The images will be stacked and saved as 
    a numpy array that will be returned. 
    '''
    imgs = []
    paths = glob(path)
    index = 0
    for p in paths:
        img = read_img(p, size)
        imgs.append(img)
        index += 1
        # info about the progress 
        if (index % 200 == 0):
            print(index)
    return np.array(imgs)