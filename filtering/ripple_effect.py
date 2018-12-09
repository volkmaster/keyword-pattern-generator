import numpy as np
from PIL import Image
import util


__author__ = 'Ziga Vucko'


def run(source_image, k=10):
    print(util.timestamp() + ' Applying filter: Ripple effect')

    tokens = source_image.split('.')
    destination_image = tokens[0] + '_rippled.' + tokens[1]

    img = Image.open(source_image)
    img = np.array(img).transpose((1, 0, 2))

    A = img.shape[0] / 3.0
    w = 2.0 / img.shape[1]

    shift = lambda x: A * np.sin(k * np.pi * x * w)

    for i in range(img.shape[0]):
        img[:, i] = np.roll(img[:, i], int(shift(i)))

    img = Image.fromarray(img.transpose((1, 0, 2)))
    img.save(destination_image)

    return destination_image
