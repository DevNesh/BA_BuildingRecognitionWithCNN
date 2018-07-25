import keras.backend as K
from keras import metrics
from keras.losses import *
from keras.preprocessing.image import ImageDataGenerator
import skimage.io as io
import skimage.transform as tr
import skimage.color
from skimage import img_as_ubyte
import numpy as np
import pandas as pd
from glob import glob

#### Read Image File for Numpy Arrays 

def read_img(path, size):
    img = io.imread(path)
    img = tr.resize(img, size)
    img_as_ubyte(img)
    return img

# Reads the images from a path, iterating over all images
# - resizing them to a 1 channel grayscale image
# - saving all images in a numpy array, returns this array 
def read_imgs(path, size):
    imgs = []
    paths = glob(path)
    index = 0
    for p in paths:
        img = read_img(p, size)
        imgs.append(img)
        index += 1
        if (index % 200 == 0):
            print(index)
    return np.array(imgs)

### Read Images By Keras Generator

def fix_mask(mask, threshold = 100):
    mask[mask < threshold] = 0.0
    mask[mask >= threshold] = 255.0

def adjustData(img,mask):
    fix_mask(mask, 100)
    img = img/255.
    mask = mask/255.
    return (img,mask)

def loadData(inputPath, outputPath, batch_size=32,save_dir=None):

    image_generator = ImageDataGenerator().flow_from_directory(inputPath, color_mode ='grayscale', target_size=(224,224), batch_size=1, class_mode=None, save_to_dir = save_dir, shuffle=False,seed=1)
    mask_generator =  ImageDataGenerator().flow_from_directory(outputPath,  color_mode ='grayscale', target_size=(224,224), batch_size=1 , class_mode=None, save_to_dir = save_dir,shuffle=False, seed=1)

    print (image_generator[0].shape)
    print (mask_generator[0].shape)

    train_generator = zip(image_generator, mask_generator)

    for (img,mask) in train_generator:
        img,mask = adjustData(img,mask)
        yield (img,mask)

def showImage(arr, i, title=None):
    if (title != None):
        plt.title(title)
        
    plt.imshow(arr[i, ..., 0], cmap = 'gray')
    plt.show()
    print(arr[i].shape)