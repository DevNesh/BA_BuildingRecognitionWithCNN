import numpy as np
import os, errno
import utils as ip
import random 
import skimage.io as io 
import scipy as sc
from skimage import data
from skimage.transform import rescale, resize
from skimage.util import random_noise
from skimage.color import rgb2gray
from PIL import Image

### Variables ###
inputPathOriginal = 'C:/Users/wohlfart/Desktop/Datenset_skyscraper/Original'
inputPathMarked =   'C:/Users/wohlfart/Desktop/Datenset_skyscraper/Marked'

outputPathMask = 'C:/Users/wohlfart/Desktop/tets/mask'
outputPathOriginal = 'C:/Users/wohlfart/Desktop/tets/image'
markedColor = 255       # 8Bit / WHITE 
imageSize = (224,224)   # size of outputimages

### Functions ###

def saveAndProcessOriginalImage(img, imgPath):

    #noise added on only 10 % of images
    #if (random.randint(0,9) == 0):
    #    img = ip.randomNoiseImage(img)
    #Image.fromarray(img).save(imgPath)
    io.imsave(imgPath, img)

#Nach der Erstellung der Maske aufrufen 
def colorToGrayScaleImage(img):
    return rgb2gray(img)

def rotateImagesByRandomAngle(img1, img2):
    randAngle = random.randint(1,40)
    img1 = ip.rotateImage(img1,randAngle)
    img2 = ip.rotateImage(img2,randAngle)
    return (img1, img2)

def changeGammaOnImages(img1, img2):
    randGamma = random.uniform(0.5,2)
    randGain = random.uniform(0.3,1)
    img1 = ip.gammaChangeImage(img1, randGamma, randGain)
    img2 = ip.gammaChangeImage(img2, randGamma, randGain)
    return (img1,img2)

def flipImagesHorizontal(img1, img2):
    return (ip.horizontalFlipImage(img1), ip.horizontalFlipImage(img2))

def flipImagesVertical(img1, img2):
    return (ip.verticalFlipImage(img1), ip.verticalFlipImage(img2))

def createDifferenceImage(img1, img2, newName):
    
    blank_image = np.zeros(imageSize, dtype=np.uint8)

    #fill every difference with white pixel 
    for x in range(img1.shape[0]):
        for y in range(img1.shape[1]):
            if (img1[x,y] != img2[x,y]):
                blank_image[x,y] = markedColor

    #erosion + dilation to remove some noise
    blank_image = ip.erosionOnImage(blank_image)
    blank_image = ip.dilationOnImage(blank_image)

    #save the mask    
    Image.fromarray(blank_image).save(outputPathMask + '/' + newName)

def preprocessingImages(img1, img2):

    resultImages = (img1, img2)
    #Random wie viele Funktionen aufgerufen werden
    iterations = random.randint(1,2)
    for i in range(0,iterations):
        randFunction = random.randint(0,2)
        #print ("** rand: ", randFunction)
        if randFunction == 0:
            resultImages = changeGammaOnImages(resultImages[0], resultImages[1])
        elif randFunction == 1:
            resultImages = flipImagesHorizontal(resultImages[0], resultImages[1])
        elif randFunction == 2:
            resultImages = rotateImagesByRandomAngle(resultImages[0], resultImages[1])

    return resultImages

def traverseOverImageFolders(directoryOriginal, directoryMarked):
    if os.path.exists(directoryOriginal):
        imagesOriginal = os.listdir(directoryOriginal)
        imagesMarked = os.listdir(directoryMarked)
        index = 0
        while index < len(imagesOriginal):

            #read the images into a np array 
            img1 = io.imread(inputPathOriginal + '/' + imagesOriginal[index], True)
            img1 = resize(img1, imageSize)
            img2 = io.imread(inputPathMarked + '/' + imagesMarked[index], True)
            img2 = resize(img2, imageSize)

            #preprocessing both images
            #images = preprocessingImages(img1,img2)
            images = (img1,img2)

            #create the mask 
            createDifferenceImage(images[0], images[1], imagesOriginal[index])
            
            #preprocessing the inputImage 
            saveAndProcessOriginalImage(images[0], outputPathOriginal + '/' + imagesOriginal[index])
            
            index += 1
            if (index % 200 == 0): print (index)
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