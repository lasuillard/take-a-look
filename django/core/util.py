""" /core/util.py
    reusable functions and classes across the application
"""
import json
import numpy as np
from tensorflow.keras.models import load_model
from keras.preprocessing import image
from joblib import load

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
        svm_featextr = load_model(meta['featextr'])
        svm_kernel = load(meta['kernel'])
    elif kind == 'dt':
        dt_featextr = svm_featextr
        dt_clf = load(meta['clf'])
    elif kind == 'cnn':
        cnn_model = load_model(meta['model'])


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
