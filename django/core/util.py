""" /core/util.py
    reusable functions and classes across the application
"""
import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from keras.preprocessing import image
from joblib import load


# metrics
def recall(y, pred):
    y = K.round(K.clip(y, 0, 1))
    pred = K.round(K.clip(pred, 0, 1))

    count_tpos = K.sum(y * pred)
    count_tposfneg = K.sum(y)

    _recall = count_tpos / (count_tposfneg + K.epsilon())
    return _recall


def precision(y, pred):
    y = K.round(K.clip(y, 0, 1))
    pred = K.round(K.clip(pred, 0, 1))

    count_tpos = K.sum(y * pred)
    count_tposfpos = K.sum(pred)

    _precision = count_tpos / (count_tposfpos + K.epsilon())
    return _precision


def f1score(y, pred):
    _recall = recall(y, pred)
    _precision = precision(y, pred)

    _f1score = (2 * _recall * _precision) / (_recall + _precision + K.epsilon())
    return _f1score


model_meta = json.load(open('ml-models.json'))

# svm
svm_featextr, svm_kernel = None, None

# deicision tree
dt_featextr, dt_clf = None, None

# cnn
cnn_model = None

for meta in model_meta:
    kind = meta['kind']
    if kind == 'svm':
        svm_featextr = load_model(meta['featextr'],
                                  custom_objects={'precision': precision,
                                                  'recall': recall,
                                                  'f1score': f1score})
        svm_kernel = load(meta['kernel'])
    elif kind == 'dt':
        dt_featextr = svm_featextr
        dt_clf = load(meta['clf'])
    elif kind == 'cnn':
        cnn_model = load_model(meta['model'],
                               custom_objects={'precision': precision,
                                               'recall': recall,
                                               'f1score': f1score})


def _preproc_img(img_file):
    img = image.load_img(img_file, target_size=(150, 150))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    return x


def predict(img, model):
    x = _preproc_img(img)
    if model == 'svm':
        x = svm_featextr.predict(x)
        y = svm_kernel.predict(x)[0]
    elif model == 'dt':
        x = dt_featextr.predict(x)
        y = dt_clf.predict(x)[0]
    elif model == 'cnn':
        y = int(cnn_model.predict(x)[0][0])
    else:
        y = None

    return y
