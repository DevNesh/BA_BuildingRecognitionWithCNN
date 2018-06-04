
import numpy as np
import os, cv2
import sklearn.utils import shuffle
import sklearn.cross_validation import train_test_split

from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD,RMSprop,adam


from keras import backend as K
K.set_image_dim_ordering('tf')

from sklearn.preprocessing import MinMaxScaler


def imageToFeatureVector(image, size=(128,128)):
    return cv2.resize(image,size).flatten()

# Parameter 
img_rows = 128
img_cols = 128
num_channel = 1
data_path = "PFAD/EINFUEGEN"

batch_size = 16
num_epoch = 

#Conainer für die Bilder
img_data_list = []
img_list = os.listdir(data_path)

#Bereitet die Daten vor und lädt sie in eine Liste 
for img in img_list:
    input_img = cv2.imread(data_path + '/' + img)
    input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    #input_img_resize = cv2.resize(input_img, (128,128))
    input_img_flatten = imageToFeatureVector(input_img, (128,128))
    #img_data_list.append(input_image_resize)    
    img_data_list.append(input_img_flatten)


img_data = np.array(img_data_list)
img_data = img_data.astype('float32')

img_data_scaled = preprocessing.scale(img_data)
img_data_scaled = img_data_scaled.reshape(img_data.shape[0], img_rows, img_cols, num_channel)


### Diesen Teil ersetzen ###

# Definiere das Ergebnis
num_classes = 4
num_of_samples = img_data.shape[0]

labels = np.ones((num_of_samples,),dtype='int64')

labels[0:102] = 0
labels[102:204] = 1
labels[204:606] = 2
labels[606:] = 3

names = ['cats','dogs','horses','humans']

Y = np_utils.to_categorical(labels, num_classes)
### 

# Zufällige Reihenfolge des Datensets 
x,y = shuffle(img_data, Y, random_state=2)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)


### DEFINING THE MODEL: Definiert die Architektur des CNN ###
input_shape = img_data_scaled[0]

model = Sequential()

model.add(Convolution2D(32, 3,3,border_mode='same',input_shape=input_shape))
model.add(Activation('relu'))
model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

model.add(Convolution2D(64, 3, 3))
model.add(Activation('relu'))
#model.add(Convolution2D(64, 3, 3))
#model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation('softmax'))

# Kompilieren des Models, Optimizer setzen 
model.compile(loss='categorial_crossentropy', optimizer='adadelta', metrics=['accuracy'])

# Trainieren des Models, Iteriert über die festgelegten Trainingsdaten 
hist = model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=num_epoch, verbose=1, validation_data=(X_test, y_test))

