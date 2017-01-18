import math

import numpy as np

from keras import backend as K
from keras.layers import Convolution2D

class MaskedConvolution2D(Convolution2D):
    def __init__(self, *args, mask='B', **kwargs):
        super().__init__(*args, **kwargs)
        self.mask_type = mask

        # TODO: Define mask here? we can use filter_size and number of filters to predict the weights shape, however, build() is still a safer place for it.
        self.mask = None

    def build(self, input_shape):
        super().build(input_shape)

        self.mask = np.ones(self.get_weights()[0].shape)

        filter_size = self.mask.shape[0]
        filter_center = filter_size / 2

        self.mask[math.ceil(filter_center):] = 0
        self.mask[math.floor(filter_center), math.ceil(filter_center):] = 0

        if self.mask is 'A':
            self.mask[math.floor(filter_center), math.floor(filter_center)] = 0

        self.mask = K.variable(self.mask)

    def call(self, x, mask=None):
        """ TODO: learn what is this mask parameter and how to use it. """
        self.W *= self.mask
        return super().call(x, mask=mask)

    def get_config(self):
        return dict(list(super().get_config().items()) + list({'mask': self.mask_type}.items()))
