#%% Imports.
import numpy as np

import keras
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import Nadam
from keras.layers.advanced_activations import PReLU
from keras.utils import np_utils
from keras.utils.visualize_util import plot
from keras import backend as K
from keras.callbacks import TensorBoard, ModelCheckpoint

from eva.models.pixelcnn import PixelCNN
from eva.util.nutil import quantisize

#%% Arguments.
batch_size = 32
nb_epoch = 200

data_augmentation = True

#%% Data.
(train, _), (test, _) = cifar10.load_data()
features = np.concatenate((train, test), axis=0)

labels = np.dot(features, [0.299, 0.587, 0.114]).reshape(features.shape[0], features.shape[1]*features.shape[2], 1).astype(int)
features = np.expand_dims(np.dot(features, [0.299, 0.587, 0.114]), -1)

# TODO: Make is scalable to any amount of channels.
# Such as: to_softmax(channel) for channel in data.shape[3].

#%% Model.
model = PixelCNN(features.shape[1:], 128, 12)

model.summary()

plot(model)

K.eval(model.get_layer(index=1).mask)[3,3]

#%% Train.
# model.fit({'input_map': features},
#           {'red': np.expand_dims(features[:, :, :, 0].reshape(features.shape[0], features.shape[1]*features.shape[2]), -1),
#           verbose=1, callbacks=[TensorBoard(), ModelCheckpoint('model.h5')])
#            'green': np.expand_dims(features[:, :, :, 1].reshape(features.shape[0], features.shape[1]*features.shape[2]), -1),
#            'blue': np.expand_dims(features[:, :, :, 2].reshape(features.shape[0], features.shape[1]*features.shape[2]), -1)},
#           batch_size=batch_size, nb_epoch=nb_epoch,

model.fit(features, labels,
          batch_size=batch_size, nb_epoch=nb_epoch,
          verbose=1, callbacks=[TensorBoard(), ModelCheckpoint('model.h5')])
