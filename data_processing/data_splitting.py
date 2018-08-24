'''
Module, can be used for splitting the data into train, test and validation set. 
'''

import numpy as np
import os, errno
import shutil
from skimage import data
from sklearn.model_selection import train_test_split

### Directories ###
foldername = 'Datenset_Block3'

inputOriginal = '/home/dan/Desktop/' + foldername + '/train/images/data'
inputMasks = '/home/dan/Desktop/' + foldername + '/train/masks/data'

testDirImages = '/home/dan/Desktop/' + foldername + '/test/images/data'
testDirMasks = '/home/dan/Desktop/' + foldername + '/test/masks/data'

valDirImages = '/home/dan/Desktop/' + foldername + '/validate/images/data'
valDirMasks = '/home/dan/Desktop/' + foldername + '/validate/masks/data'

proportionOfValidateAndTestData = 0.3

### Functions ###
def splitContent(imagePath, maskPath):
    '''
    Function splits the data into a validation and a testing part.
    '''
    
    images = os.listdir(imagePath)
    masks = os.listdir(maskPath)

    train_images, test_images ,train_masks, test_masks = train_test_split(images, masks, test_size=proportionOfValidateAndTestData, random_state=42)
    test_images, validate_images, test_masks, validate_masks = train_test_split(test_images, test_masks, test_size=0.5, random_state=42)

    index = 0
    while index < len(test_images):
        shutil.move(inputOriginal + '/' + test_images[index], testDirImages + '/' + test_images[index])
        shutil.move(inputMasks + '/' + test_masks[index], testDirMasks + '/' + test_masks[index])
        index += 1

    index = 0
    while index < len(validate_images):
        shutil.move(inputOriginal + '/' + validate_images[index], valDirImages + '/' + validate_images[index])
        shutil.move(inputMasks + '/' + validate_masks[index], valDirMasks + '/' + validate_masks[index])
        index += 1        


### Calls ###
if (os.path.exists(inputOriginal) and os.path.exists(inputMasks)):

     #check for existing validation path for images, if not make one
    if not os.path.exists(valDirImages):
        try:
            os.makedirs(valDirImages)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    #check for existing validation path for masks, if not make one
    if not os.path.exists(valDirMasks):
        try:
            os.makedirs(valDirMasks)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

     #check for existing test path for images, if not make one
    if not os.path.exists(testDirImages):
        try:
            os.makedirs(testDirImages)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    #check for existing test path for amsks, if not make one
    if not os.path.exists(testDirMasks):
        try:
            os.makedirs(testDirMasks)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    splitContent(inputOriginal, inputMasks)
else:
    print ('The inputPath or maskPath does not exist')
