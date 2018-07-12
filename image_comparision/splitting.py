import numpy as np
import os, errno
import random
import skimage.io as io
import shutil
from skimage import data
from skimage.transform import rescale, resize
from skimage.util import random_noise
from skimage.color import rgb2gray
from sklearn.model_selection import train_test_split


foldername = 'testbild'

### Variables ###
inputOriginal = '/home/dan/Desktop/' + foldername + '/train/images/data'
inputMasks = '/home/dan/Desktop/' + foldername + '/train/masks/data'

testDirImages = '/home/dan/Desktop/' + foldername + '/test/images/data'
testDirMasks = '/home/dan/Desktop/' + foldername + '/test/masks/data'

valDirImages = '/home/dan/Desktop/' + foldername + '/validate/images/data'
valDirMasks = '/home/dan/Desktop/' + foldername + '/validate/masks/data'


### Functions ###

def traverseOverImageFolders(directoryOriginal):
    if os.path.exists(directoryOriginal):

        images = os.listdir(inputOriginal)
        masks = os.listdir(inputMasks)

        train_images, test_images ,train_masks, test_masks = train_test_split(images, masks, test_size=0.3, random_state=42)
        test_images, validate_images, test_masks, validate_masks = train_test_split(test_images, test_masks, test_size=0.5, random_state=42)

        print(len(validate_images))
        print(len(validate_masks))
        print(len(test_images))
        print(len(test_masks))

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
    else:
        print ('The following path does not exists:',directoryOriginal)


### Calls ###
if (os.path.exists(inputOriginal)):

    traverseOverImageFolders(inputOriginal)

else:
    print ('The inputPath does not exist')
