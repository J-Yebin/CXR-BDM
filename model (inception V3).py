# -*- coding: utf-8 -*-
"""[CXR-BDM] Keras_INCEPTION.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TgE8WE8DwTySvEfeXRYmpbniIsIIt_UW
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install pydicom

import matplotlib.pyplot as plt
import pickle
import gzip
import numpy as np
import pydicom as dicom
import cv2

#data
from sklearn.model_selection import train_test_split

# Augmentation
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Modeling
from tensorflow import keras
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D

basic_path = '/content/drive/MyDrive/Endo-CXR'

with gzip.open(basic_path+'/x_train_299.pickle', 'rb')as f:
    x_train_299 = pickle.load(f) #pixel arrays resized to 299x299

with gzip.open(basic_path + '/y_target.pickle', 'rb') as f:
    y_target = pickle.load(f)



x_train, x_test, y_train, y_test = train_test_split(x_train_299, y_target, test_size=0.2, random_state=321)



#data augmentaion
train_datagen = ImageDataGenerator(
    samplewise_center=True, 
    samplewise_std_normalization= True, 
    rotation_range = 20, 
    shear_range = 0.02,
    zoom_range = 0.02, 
    horizontal_flip=True)

test_datagen = ImageDataGenerator()

# Flow training images in batches of 20 using train_datagen generator
train_generator = train_datagen.flow(x_train, y_train, batch_size=20)

# Flow validation images in batches of 20 using test_datagen generator
validation_generator = test_datagen.flow(x_test, y_test, batch_size=20)

#model hyperparameters
IMG_SIZE = 299
N_CLASS = 2
N_EPOCHS = 50
N_BATCH = 100
steps_per_epoch = len(x_train) / N_BATCH
validation_steps = int(np.ceil(len(x_test) / N_BATCH))

#model
inceptionV3 = InceptionV3(
    weights='imagenet',
    include_top=False, 
    input_shape=(IMG_SIZE, IMG_SIZE, 3))

def create_Inception_model():
    model = keras.Sequential()
    model.add(inceptionV3)
    model.add(GlobalAveragePooling2D())
    model.add(Dense(1024, activation='relu'))
    model.add(Dense(2, activation='softmax'))
    return model

from sklearn.utils.class_weight import compute_class_weight

y_integers = np.argmax(y_train, axis=1)
class_weights = compute_class_weight('balanced', np.unique(y_integers), y_integers)
d_class_weights = dict(enumerate(class_weights))

model = create_Inception_model()

model.compile(loss="categorical_crossentropy", 
              optimizer="adam", 
              metrics=["accuracy"])

history = model.fit(
    train_generator, 
    validation_data=validation_generator, 
    batch_size=N_BATCH, 
    steps_per_epoch=steps_per_epoch, 
    epochs=N_EPOCHS,
    class_weight=d_class_weights)

'''
#saving model
from keras.models import load_model
model.save('cxr_inception_ClassWeight.h5')

#saving history
np.save('cxr_inception_ClassWeight_history.npy',history.history)
'''

from keras.models import load_model
model = load_model('/content/drive/MyDrive/cxr_inception_ClassWeight.h5')

history=np.load('/content/drive/MyDrive/cxr_inception_ClassWeight_history.npy',allow_pickle='TRUE').item()



#accuracy and val_accuracy plot
acc = history['accuracy']
val_acc = history['val_accuracy']
loss = history['loss']
val_loss = history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'r', label='Training accuracy')
plt.plot(epochs, val_acc, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend(loc=0)
plt.figure()
plt.show()



#auroc
from sklearn.metrics import roc_curve
y_pred_keras = model.predict(x_test)
fpr_keras, tpr_keras, thresholds_keras  = roc_curve(y_test.argmax(axis=1), y_pred_keras.argmax(axis=1))

from sklearn.metrics import auc
auc_keras = auc(fpr_keras, tpr_keras)

plt.figure(1)
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr_keras, tpr_keras, label='Keras (area = {:.3f})'.format(auc_keras))
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('ROC curve')
plt.legend(loc='best')
plt.show()