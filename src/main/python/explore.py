#! /usr/bin/env python2
'''data analysis steps'''

### to use tf 2.0
# import pkg_resources
# pkg_resources.require("tensorflow==2.0.0a0")
from PIL import Image, ImageFile

import numpy as np
import tensorflow as tf
from tensorflow import keras

import tensorflow_hub as hub
from tensorflow.keras import layers

ImageFile.LOAD_TRUNCATED_IMAGES = True
tf.enable_v2_behavior()

def unpickle(filename):
    '''load cifar images from https://www.cs.toronto.edu/~kriz/cifar.html'''
    import cPickle
    with open(filename, 'rb') as file_object:
        data = cPickle.load(file_object)
    return data

# show single image
cifar = unpickle("./images/cifar-100-python/train")
def to_image(image):
    bands = imagae.reshape(96, 3072/96)
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

# classifying on-disk data
train_datagen = keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)
train_generator = train_datagen.flow_from_directory(
    '/tmp/test',
    target_size=(150, 150),
    batch_size=32, class_mode="sparse")
validation_generator = train_datagen.flow_from_directory(
    '/tmp/test',
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
# reuse net, see https://www.tensorflow.org/tutorials/images/hub_with_keras

classifier_url = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/classification/2" #@param {type:"string"}
def classifier(x):
    classifier_module = hub.Module(classifier_url)
    return classifier_module(x)

IMAGE_SIZE = hub.get_expected_image_size(hub.Module(classifier_url))

import tensorflow.keras.backend as K
sess = K.get_session()
init = tf.global_variables_initializer()

classifier_layer = layers.Lambda(classifier, input_shape = IMAGE_SIZE+[3])
classifier_model = tf.keras.Sequential([classifier_layer])


sess.run(init)

feature_extractor_url = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/2" #@param {type:"string"}
feature_extractor_layer = hub.KerasLayer(feature_extractor_url,
                                         input_shape=(224,224,3))
feature_batch = feature_extractor_layer(image_batch)
print(feature_batch.shape)
feature_extractor_layer.trainable = False
model = tf.keras.Sequential([
  feature_extractor_layer,
  layers.Dense(image_data.num_classes, activation='softmax')
])
# todo: save and use in tf.js

# try cnn
model = keras.Sequential([
    keras.layers.Conv2D(64, 3, input_shape=(150, 150, 3)),
    keras.layers.MaxPool2D(2),
    keras.layers.Conv2D(32, 2),
    keras.layers.MaxPool2D(2),
    keras.layers.Flatten(),
    keras.layers.Dense(180, activation=tf.nn.relu),
    keras.layers.Dense(180, activation=tf.nn.relu),
    keras.layers.Dense(3, activation=tf.nn.softmax)
])
# use mobilenet model https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/2
num_classes=3
IMAGE_SIZE=[224,224]

train_datagen = keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)
train_generator = train_datagen.flow_from_directory(
    '/tmp/test',
    target_size=IMAGE_SIZE,
    batch_size=32, class_mode="sparse")
validation_generator = train_datagen.flow_from_directory(
    '/tmp/test',
    target_size=IMAGE_SIZE,
    batch_size=32, class_mode="sparse")
model = tf.keras.Sequential([
    hub.KerasLayer(
        "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/2",
        output_shape=[1280],
        trainable=False),  # Can be True, see below.
    tf.keras.layers.Dense(num_classes, activation='softmax')
])
model.build([None, 224, 224, 3]) # Batch input shape.
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit_generator(train_generator, steps_per_epoch=400, epochs=5,
                    validation_data=validation_generator, validation_steps=40)
