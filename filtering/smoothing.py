import cv2
import util


__author__ = 'Ziga Vucko'


def run(source_image, kernel_size=5):
    print(util.timestamp() + ' Applying filter: Smoothing')

    tokens = source_image.split('.')
    destination_image = tokens[0] + '_smoothed.' + tokens[1]

    img = cv2.imread(source_image)
    blur = cv2.blur(img, (kernel_size, kernel_size))

    cv2.imwrite(destination_image, blur)

    return destination_image
