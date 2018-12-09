# This file is part of Pixelsorting.
#
# Pixelsorting is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelsorting is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pixelsorting.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import logging
from math import sqrt

from PIL import Image

from filtering.pixelsorter.keys import luma
from filtering.pixelsorter.util import coords_to_index

# get logger for current script (even across different modules)
logger = logging.getLogger(__name__)


def edge_detect(image, size):
    """
    Applies a Sobel filter to the given image.
    :param image: An image as a list of (R,G,B) values
    :param size: The size of the image as a tuple (width, height)
    :return: An array of the Sobel gradient value of each image pixel
    This value roughly corresponds to how much of an "edge" a pixel is.
    """
    # TODO get edge data for boundaries
    width, height = size
    edge_data = [0] * len(image)
    gray_scale_img = list(map(luma, image))
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            idx = coords_to_index((x, y), width)

            a, b, c = gray_scale_img[idx - 1 - width: idx + 2 - width]
            d, e, f = gray_scale_img[idx - 1: idx + 2]
            g, h, i = gray_scale_img[idx - 1 + width: idx + 2 + width]

            g_x = -a - 2 * d - d + c + 2 * f + i
            g_y = -a - 2 * b - c + g + 2 * h + i

            g = sqrt(g_x * g_x + g_y * g_y)
            edge_data[idx] = g

            if idx % 200000 == 0:
                logger.info("Edge detection done for %d / %d pixels... (%2.2f%%)" %
                            (idx, width * height, 100 * idx / float(width * height)))
    return edge_data


def highlight_threshold(image, img_data, threshold, color=(255, 0, 0)):
    """
    Given an array of values for an image, highlights pixels whose value is greater than the given threshold.
    :param image: The image to highlight
    :param img_data: The values to use
    :param threshold: The threshold above which pixels should the highlighted
    :param color: The color to highlight pixels with
    :return: The image, with high-value pixels highlighted
    """
    out_pixels = list(image)
    for i in range(len(image)):
        p, e = image[i], img_data[i]
        if e > threshold:
            out_pixels[i] = color
    return out_pixels


def main():
    # set up command line argument parser
    parser = argparse.ArgumentParser(description='A tool for pixel-sorting images')
    parser.add_argument("infile", help="The input image")
    parser.add_argument("-o", "--outfile", required=True, help="The output image")
    parser.add_argument("-t", "--threshold", type=float, required=True, help="Edge detection threshold")

    args = parser.parse_args()

    # load image
    img = Image.open(args.infile)
    original_pixels = list(img.getdata())

    edge_data = edge_detect(original_pixels, img.size)
    out_pixels = highlight_threshold(original_pixels, edge_data, threshold=args.threshold)

    # write output image
    img_out = Image.new(img.mode, img.size)
    img_out.putdata(out_pixels)
    img_out.save(args.outfile)


if __name__ == '__main__':
    main()
