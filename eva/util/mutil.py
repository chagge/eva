import numpy as np


def infer(model):
    pixels = np.zeros(model.input_shape[1:])
    rows, cols, channels = pixels.shape
    for row in range(rows):
        for pixel in range(cols):
            for channel in range(channels):
                pixels[row, pixel, channel] = model.predict_on_batch(pixels[np.newaxis])[0][row, pixel, channel]

    return pixels
