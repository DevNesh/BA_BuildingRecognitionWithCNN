import numpy as np
import cv2 as cv2
import os, errno

### Variables ###
inputPathOriginal = 'C:/Users/wohlfart/Desktop/dataset2/Original'
inputPathMarked = 'C:/Users/wohlfart/Desktop/dataset2/Marked'

outputPathMask = 'C:/Users/wohlfart/Desktop/dataset2/masks'
outputPathOriginal = 'C:/Users/wohlfart/Desktop/dataset2/images'
markedColor = (255, 255, 255)

### Functions ###

def stop(): 
    img = cv2.imread('Example2_red.PNG',0)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

def createDifferenceImage(image1, image2):

    test1 = cv2.cv.LoadImage(inputPathOriginal + '/' + image1)
    test2 = cv2.cv.LoadImage(inputPathMarked + '/' + image2)
    blank_image = np.zeros((test1.height,test1.width,3), np.uint8)

    for x in range(test1.height):
        for y in range(test2.width):
            if (test1[x,y] != test2[x,y]):
                blank_image[x,y] = markedColor
    
    cv2.imwrite(outputPathMask + '/' + image1,blank_image)
    cv2.imwrite(outputPathOriginal + '/' + image1, cv2.imread(inputPathOriginal + '/' + image1))


def traverseOverImageFolders(directoryOriginal, directoryMarked):
    if os.path.exists(directoryOriginal):
        imagesOriginal = os.listdir(directoryOriginal)
        imagesMarked = os.listdir(directoryMarked)
        index = 0
        while index < len(imagesOriginal):
            img1 = imagesOriginal[index]
            img2 = imagesMarked[index]
            createDifferenceImage(img1, img2)
            index += 1
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