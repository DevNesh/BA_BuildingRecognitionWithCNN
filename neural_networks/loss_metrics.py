import keras.backend as K
from keras import metrics
from keras.losses import *


def f1(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + 1.) / (K.sum(y_true_f) + K.sum(y_pred_f) + 1.)

def f1_np(y_true, y_pred):
    return (2. * (y_true * y_pred).sum() + 1.) / (y_true.sum() + y_pred.sum() + 1.)

def f1_loss(y_true, y_pred):
    return 1-f1(y_true, y_pred)

def f2(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (5. * intersection + 1.) / (4. * K.sum(y_true_f) + K.sum(y_pred_f) + 1.)

def f2_loss(y_true, y_pred):
    return 1-f2(y_true, y_pred)

def iou(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (intersection + 1.) / (K.sum(y_true_f) + K.sum(y_pred_f) + 1. - intersection)

def iou_np(y_true, y_pred):
    intersection = (y_true * y_pred).sum()
    return (intersection + 1.) / (y_true.sum() + y_pred.sum() + 1. - intersection)

def iou_loss(y_true, y_pred):
    return -iou(y_true, y_pred)

def precision(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (intersection + 1.) / (K.sum(y_pred_f) + 1.)

def precision_np(y_true, y_pred):
    return ((y_true * y_pred).sum() + 1.) / (y_pred.sum() + 1.)

def recall(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (intersection + 1.) / (K.sum(y_true_f) + 1.)

def recall_np(y_true, y_pred):
    return ((y_true * y_pred).sum() + 1.) / (y_true.sum() + 1.)

def mae_img(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    return mae(y_true_f, y_pred_f)

def bce_img(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    return binary_crossentropy(y_true_f, y_pred_f)

def f1_bce(y_true, y_pred):
    return f1_loss(y_true, y_pred) + bce_img(y_true, y_pred)

# FP + FN
def error(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    return K.sum(K.abs(y_true_f - y_pred_f)) / float(224*224)

def error_np(y_true, y_pred):
    return (abs(y_true - y_pred)).sum() / float(len(y_true.flatten()))