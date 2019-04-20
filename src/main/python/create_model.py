# needs: pip install tf-nightly-2.0-preview tensorflow_hub
from PIL import Image, ImageFile

import numpy as np
import tensorflow as tf
from tensorflow import keras

import tensorflow_hub as hub
from tensorflow.keras import layers

ImageFile.LOAD_TRUNCATED_IMAGES = True

IMAGE_SIZE = [224, 224]

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


# from https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/2
model = tf.keras.Sequential([
    hub.KerasLayer("https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/2", output_shape=[1280], trainable=False),
    tf.keras.layers.Dense(train_generator.num_classes, activation='softmax')
])
model.build([None] + IMAGE_SIZE + [3])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.fit_generator(train_generator, steps_per_epoch=400, epochs=5,
                    validation_data=validation_generator, validation_steps=40)

# from https://www.tensorflow.org/alpha/guide/keras/saving_and_serializing
model.save('/tmp/path_to_my_model.h5')

# Recreate the exact same model purely from the file
#new_model = keras.models.load_model('path_to_my_model.h5')
