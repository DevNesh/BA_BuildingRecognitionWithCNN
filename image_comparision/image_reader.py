import numpy as np
import cv2 as cv2
import os, errno

### Variables ###
inputPath = 'C:/Users/wohlfart/Desktop/test/Input'
outputPath = 'C:/Users/wohlfart/Desktop/test/Output'
markedColor = (0.0, 0.0, 255)

### Functions ###

def stop(): 
    img = cv2.imread('Example2_red.PNG',0)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

def createDifferenceImage(image1, image2):

    test1 = cv2.cv.LoadImage(inputPath + '/' + image1)
    test2 = cv2.cv.LoadImage(inputPath + '/' + image2)
    blank_image = np.zeros((test1.height,test1.width,3), np.uint8)

    for x in range(test1.height):
        for y in range(test2.width):
            if (test1[x,y] != test2[x,y]):
                blank_image[x,y] = markedColor
    
    resultName = image1.split('.',1)
    resultName = resultName[0] + '_output.png'

    resultName = outputPath + '/' + resultName
    cv2.imwrite(resultName,blank_image)


def traverseOverImageFolder(directory):
    if os.path.exists(directory):
        images = os.listdir(directory)
        index = 0
        while index < len(images):
            img1 = images[index]
            img2 = images[index+1]
            createDifferenceImage(img1, img2)
            index += 2
    else:
        print ('The following path does not exists:',directory)


### Calls ###  
if (os.path.exists(inputPath)):
    
    #check for existing output path, if not make one
    if not os.path.exists(outputPath):
        try:
            os.makedirs(outputPath)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    traverseOverImageFolder(inputPath)

else:
    print ('The inputPath does not exist')