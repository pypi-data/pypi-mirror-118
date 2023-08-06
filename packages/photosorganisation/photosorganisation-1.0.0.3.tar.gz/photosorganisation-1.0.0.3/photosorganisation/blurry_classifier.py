'''Imports'''
from tensorflow.keras import models
from photosorganisation.data import get_image_dict
import os
import cv2
import numpy as np
import shutil
import joblib
import sys
def blurry_classifier(folder_path):
    print("Looking for Blurry Photos...", "black", "on_white")
    loca_path = os.path.dirname(__file__)
    model_path = os.path.join(loca_path, "trained_models", "blur_detector.h5")
    #model_path = "photosorganisation/trained_models/blur_detector.h5"
    pipeline = models.load_model(model_path)

    path = folder_path
    #path = os.path.join('.', 'raw_data', 'test_mantha')

    img_dict = get_image_dict(path, size = (200,200))
    blurry_dump = os.path.join(path,'Blurry')


    if not os.path.exists(blurry_dump):
        os.mkdir(blurry_dump)



    for k in img_dict.keys():
        pred = pipeline.predict(np.expand_dims(img_dict[k], axis = 0))
        if pred > 0.5:
            shutil.move((os.path.join(path, k)), (os.path.join(path, 'Blurry', k)))
