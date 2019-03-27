#! /usr/bin/env python2

# to use tf 2.0
import pkg_resources
pkg_resources.require("tensorflow==2.0.0a0")

import tensorflow as tf
from tensorflow import keras
import numpy as np



def unpickle(file):
    '''load cifar images from https://www.cs.toronto.edu/~kriz/cifar.html'''
    import cPickle
    with open(file, 'rb') as fo:
        dict = cPickle.load(fo)
    return dict

# show single image
cifar = unpickle("./images/cifar-100-python/train")
pic = train['data'][0].reshape(96, 3072/96)
c = Image.merge("RGB", map(Image.fromarray, [pic[:32], pic[32:64], pic[64:]]))

# try to classify
model = keras.Sequential([
           keras.layers.Dense(3072, activation=tf.nn.relu),
           keras.layers.Dense(3072, activation=tf.nn.relu),
           keras.layers.Dense(3072, activation=tf.nn.relu),
           keras.layers.Dense(100, activation=tf.nn.softmax)
       ])
model.compile(optimizer='adam', 
                     loss='sparse_categorical_crossentropy',
                     metrics=['accuracy'])
model.fit(cifar['data'], np.array(cifar['fine_labels']), epochs=5)
test = unpickle("./images/cifar-100-python/test")
test_loss, test_acc = model.evaluate(test['data'], np.array(test['fine_labels']))
