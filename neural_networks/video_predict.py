import numpy as np 
import cv2 
import skimage.transform as tr

videoPath = "C:/Users/wohlfart/Desktop/testvideo.mp4"
capture = cv2.VideoCapture(videoPath)

i = 0

while (capture.isOpened()):
    ret, frame = capture.read()
    
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = tr.resize(img,(224,224,1))
    test = np.asarray(img, dtype="int32")


    print(test.shape)

    cv2.imshow('frame',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    i+=1

capture.release()
cv2.destroyAllWindows()