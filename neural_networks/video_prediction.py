# coding: utf-8
from keras.models import load_model
from keras.models import model_from_json
from keras.optimizers import *
import numpy as np 
import cv2 
import math
import skimage.transform as tr
import skimage.io as io
from skimage import img_as_ubyte

from loss_metrics import *
from helper import * 


IMG_PATH = "C:/Users/wohlfart/Desktop/testbild.jpg"
VID_PATH = "C:/Users/wohlfart/Videos/testvideo.mp4"
MODEL_JSON = "model_test.json"
MODEL_WEIGHTS = "model_test.h5" 


###### Functions ######

'''
Function, loads the trained Neural Network for prediction.
'''
def loadModel(jsonPath, weightsPath):

    json_file = open(jsonPath, encoding="utf8")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    # load weights into new model
    loaded_model.load_weights(weightsPath)
    print("Loaded model from disk")

    # evaluate loaded model on test data
    loaded_model.compile(optimizer=Adam(lr=0.0001), loss=iou_loss)

    return loaded_model

'''
Function, predict an image and draws a rectangle around the predicted image.
'''
def predict(model,frame,grayscale,showResult):

    # convert to the right format and predict
    if (not grayscale):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        img = frame

    multX = img.shape[1] / 224
    multY = img.shape[0] / 224 

    img = tr.resize(img,(224,224,1))
    img = np.expand_dims(img, axis=0)

    #predict
    pred = model.predict(img)    
    pred = img_as_ubyte(pred[0])

    # search for white areas in picture
    _,contours, hier = cv2.findContours(pred,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    if (len(contours) > 0):

        # draws a rectangle over the biggest area, get values for 
        biggest = max(contours, key=cv2.contourArea)

        if cv2.contourArea(biggest) > 20 :
            (x,y,w,h) = cv2.boundingRect(biggest)
            
            # scale the values to the original size 
            x *= multX
            x = math.ceil(x)
            y *= multY
            y = math.ceil(y)

            w *= multX
            w = math.ceil(w)
            h *= multY
            h = math.ceil(h)

            # drawing
            cv2.rectangle(frame,(x,y),(x+w,y+h),(225,255,255),1)
            cv2.putText(frame,'Tower',(x+w,y),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,255))

        if (showResult):
            cv2.imshow('Prediction',frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    return frame

def loadPicture(model):
    img = io.imread(IMG_PATH)
    predict(model, img,True, True)

'''
Function, loads a video and processes a prediction with a neural network
'''
def loadVideo(model):
    # load the video
    capture = cv2.VideoCapture(VID_PATH)

    # predict the frame
    i = 0

    while (capture.isOpened()):
        ret, frame = capture.read()
        
        result = predict(model,frame,False,False)

        cv2.imshow('frame',result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        i+=1

    capture.release()
    cv2.destroyAllWindows()


###### Executable Code ######
model = loadModel(MODEL_JSON, MODEL_WEIGHTS)
loadPicture(model)
loadVideo(model)



