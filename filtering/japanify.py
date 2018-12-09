#!/usr/bin/python3

# Original code by vvdr12: https://gist.github.com/vvdr12/6327611

from PIL import Image
import util
try:
    from tqdm import tqdm
except ImportError:  # optional dependency, simply print a X/Y ratio on each step else
    def tqdm(iterable, total):  # fallback
        for j, _ in enumerate(iterable):
            if j % 100 == 0:
                yield ''  # print(f'{j} / {total}')


def run(source_image, density=20):
    print(util.timestamp() + ' Applying filter: Japanify')

    tokens = source_image.split('.')
    destination_image = tokens[0] + '_japanified.' + tokens[1]

    img = Image.open(source_image)

    img_height = img.size[1]
    list(tqdm(japanify(img, density), total=img_height))
    img.save(destination_image)

    return destination_image


def japanify(img, threshold):
    width, height = img.size
    img = img.load()  # getting PixelAccess
    for j in range(height):
        contrast = contrastpoints(img, j - 1 if j else 0, width, threshold) # computing contrast of previous row
        m = 0
        for i in range(width):
            if m < len(contrast) and i >= contrast[m]:
                img[i, j] = (0, 0, 0)  # black
                m += 1
        yield 'ROW_COMPLETE'  # progress tracking


def contrastpoints(img, j, width, threshold):
    contrast = []
    for i in range(width - 3):
        ave1 = sum(img[i + 0, j][:3]) / 3
        ave2 = sum(img[i + 1, j][:3]) / 3
        ave3 = sum(img[i + 2, j][:3]) / 3
        ave4 = sum(img[i + 3, j][:3]) / 3
        if abs(ave2 - ave1) > threshold and abs(ave1 - ave3) > (threshold / 2):
            contrast.append(i)
    return contrast
