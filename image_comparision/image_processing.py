
# coding: utf-8

#get_ipython().run_line_magic('matplotlib', 'inline')
#import matplotlib.pyplot as plt

import skimage.io as io
from skimage import data
from skimage.transform import rescale, resize, rotate
from skimage.morphology import erosion, dilation
import warnings
from skimage.color import rgb2gray
from skimage.util import random_noise
import numpy as np
from skimage import exposure
import scipy.misc
warnings.filterwarnings("ignore")



### General functions
'''
def show_images(before, after, op):
    fig, axes = plt.subplots(nrows=1, ncols=2)
    ax = axes.ravel()
    ax[0].imshow(before, cmap='gray')
    ax[0].set_title("Original image")

    ax[1].imshow(after, cmap='gray')
    ax[1].set_title(op + " image")
    if op == "Rescaled":
        ax[0].set_xlim(0, 400)
        ax[0].set_ylim(300, 0)
    else:        
        ax[0].axis('off')
        ax[1].axis('off')
    plt.tight_layout()
'''

def read_image(path):
    return np.asarray(io.imread(path))    


### Functions, that have to be used for Original + Mask    
def horizontalFlipImage(img):
    return img[:, ::-1]

def verticalFlipImage(img):
    return img[::-1, :]

def rescaleImage(img, xScale, yScale, antialiasing):
    return resize(img, (xScale,yScale), antialiasing)

def rotateImage(img, angle):
    return rotate(img, angle)


### Functions , only for the original images
def colorToGrayScaleImage(img):
    return rgb2gray(img)

def randomNoiseImage(img):
    return random_noise(img)
    
def gammaChangeImage(img, gamma, gain):
    return exposure.adjust_gamma(img, gamma=gamma, gain=gain)
    


### Functions, only for the masks
def erosionOnImage(img):
    return erosion(img)

def dilationOnImage(img):
    return dilation(img)


'''
# Testcode
path = 'C:/Users/wohlfart/Desktop/images/screenshot841.png'

x = read_image('C:/Users/wohlfart/Desktop/screenshot296.png')
y = erosionOnImage(x)

#show_images(x, y, "Random noise")
plt.imshow(x)
plt.show()
plt.imshow(y)
plt.show()
#plt.imshow(y[i, ..., 0], cmap='gray')
#plt.show()
'''

