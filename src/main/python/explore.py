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
def to_image(byte_1d):
    bands = byte_1d.reshape(96, 3072/96)
    return Image.merge(
        "RGB", map(Image.fromarray, (bands[:32], bands[32:64], bands[64:])))
COW = to_image(cifar['data'][0])  # name: cifar['filenames'][i].split("_s_")[0]
COW.show()

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

# classifying on-disk data, see README for challenge data, should be in images/
train_datagen = keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)
train_generator = train_datagen.flow_from_directory(
    'test',
    target_size=(150, 150),
    batch_size=32, class_mode="sparse")
validation_generator = train_datagen.flow_from_directory(
    'test',
    target_size=(150, 150),
    batch_size=32, class_mode="sparse")

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(150, 150, 3)),
    keras.layers.Dense(180, activation=tf.nn.relu),
    keras.layers.Dense(180, activation=tf.nn.relu),
    keras.layers.Dense(3, activation=tf.nn.softmax)
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit_generator(train_generator, steps_per_epoch=400, epochs=5,
                    validation_data=validation_generator, validation_steps=40)
