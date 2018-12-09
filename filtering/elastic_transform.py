import numpy as np
from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter
from PIL import Image
import util


__author__ = 'Ziga Vucko'


def run(source_image, alpha, sigma, random_state=None):
    print(util.timestamp() + ' Applying filter: Elastic transform (liquify)')

    tokens = source_image.split('.')
    destination_image = tokens[0] + '_liquified.' + tokens[1]

    image = Image.open(source_image)
    image = np.array(image)

    if random_state is None:
        random_state = np.random.RandomState(None)

    shape = image.shape
    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    dz = np.zeros_like(dx)

    x, y, z = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]), np.arange(shape[2]))
    indices = np.reshape(y.transpose((1, 0, 2)) + dy, (-1, 1)), \
              np.reshape(x.transpose((1, 0, 2)) + dx, (-1, 1)), \
              np.reshape(z.transpose((1, 0, 2)), (-1, 1))

    distored_image = map_coordinates(image, indices, order=1, mode='reflect')
    distored_image = distored_image.reshape(image.shape)

    image = Image.fromarray(distored_image)
    image = image.rotate(-90)
    image.save(destination_image)

    return destination_image
