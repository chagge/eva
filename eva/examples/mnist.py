#%% Setup.
from collections import namedtuple

import numpy as np

import keras
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
from eva.models.gated_pixelcnn import GatedPixelCNN

#%% Data.
(train, _), (test, _) = mnist.load_data()
data = np.concatenate((train, test), axis=0)
data = data.astype('float32')
data /= 255
data = np.repeat(np.expand_dims(data, -1), 3, -1)

#%% Model.
# model = PixelCNN(data.shape[1:], 126, 1)
model = GatedPixelCNN(data.shape[1:], 126, 1)

model.summary()

plot(model)

#%% Train.
model.fit(data,
          [(np.expand_dims(data[:, :, :, 0].reshape(data.shape[0], data.shape[1]*data.shape[2]), -1)*255).astype(int),
           (np.expand_dims(data[:, :, :, 1].reshape(data.shape[0], data.shape[1]*data.shape[2]), -1)*255).astype(int),
           (np.expand_dims(data[:, :, :, 2].reshape(data.shape[0], data.shape[1]*data.shape[2]), -1)*255).astype(int)],
          batch_size=32, nb_epoch=40,
          verbose=1, callbacks=[TensorBoard(), ModelCheckpoint('model.h5', save_weights_only=True)]) # Only weights because Keras is a bitch.
