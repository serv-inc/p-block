"""generates tfjs model from files"""
import os

import numpy as np
import tensorflow as tf

assert tf.__version__.startswith("2")

from tflite_model_maker import model_spec
from tflite_model_maker import image_classifier
from tflite_model_maker.config import ExportFormat
from tflite_model_maker.config import QuantizationConfig
from tflite_model_maker.image_classifier import DataLoader

import matplotlib.pyplot as plt

IMAGE_PATH = "/home/uni/storage/p-block/"
MODEL_PATH = "/home/uni/repo/p-block/generated-model"
data = DataLoader.from_folder(IMAGE_PATH)
train_data, test_data = data.split(0.9)

model = image_classifier.create(train_data)
# loss, accuracy = model.evaluate(test_data)
# 0.9273504018783569
# 0.3174212872982025
# model.export('/home/uni/repo/p-block/generated-model')
model.export(MODEL_PATH, export_format=ExportFormat.TFJS)
