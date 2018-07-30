import numpy as np
import os, errno
import skimage.io as io 
from PIL import Image


def compareMasks(prediction, groundTruth):
    
    diff_img = np.zeros((252,261,3), dtype=np.uint8)

    for x in range(prediction.shape[0]):
        for y in range(prediction.shape[1]):
            if ((prediction[x,y] == groundTruth[x,y]) & groundTruth[x,y].all() != False):
                diff_img[x,y] = (255,255,255)
            elif (prediction[x,y] > groundTruth[x,y]):
                diff_img[x,y] = (255,0,0)
            elif (groundTruth[x,y] > prediction[x,y]):
                diff_img[x,y] = (0,255,0)

    return diff_img  
 


img1 = io.imread('/home/dan/Desktop/pred.png', True)
img2 = io.imread('/home/dan/Desktop/gt.png', True)

result = compareMasks(img1, img2)
Image.fromarray(result).save('/home/dan/Desktop/diff1.png')

