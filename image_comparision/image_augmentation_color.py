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
inputPathOriginal = 'C:/Users/wohlfart/Desktop/Datenset_iteration/focus/Original/data'
inputPathMarked = 'C:/Users/wohlfart/Desktop/Datenset_iteration/focus/Marked'

outputPathMask = 'C:/Users/wohlfart/Desktop/Datenset_iteration/focus/masksCOLORED'
outputPathOriginal = 'C:/Users/wohlfart/Desktop/Datenset_iteration/focus/imagesCOLORED'
markedColor = (255, 255, 255)

### Functions ###

def saveAndProcessOriginalImage(img, imgPath):
    img = resize(img, (224,224))
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
    
    blank_image = np.zeros((img1.shape[0],img1.shape[1],3), np.uint8)
    img1 = rgb2gray(img1)
    img2 = rgb2gray(img2)

    #fill every difference with white pixel 
    for x in range(img1.shape[0]):
        for y in range(img1.shape[1]):
            if (img1[x,y] != img2[x,y]):
                blank_image[x,y] = markedColor
    
    #erosion + dilation to remove some noise
    blank_image = ip.erosionOnImage(blank_image)
    blank_image = ip.dilationOnImage(blank_image)

    #save the mask    
    blank_image = rgb2gray(blank_image)
    blank_image = resize(blank_image,(224,224))
    io.imsave(outputPathMask + '/' + newName,blank_image)

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
            img1 = io.imread(inputPathOriginal + '/' + imagesOriginal[index], False) 
            img2 = io.imread(inputPathMarked + '/' + imagesMarked[index], False)

            #preprocessing both images
            images = preprocessingImages(img1,img2)

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