#!/usr/bin/python3

# Idea from vvdr12: https://www.reddit.com/r/glitch_art/comments/1p5mno/elephant_hill/ccyzbn1/

from bisect import bisect_left  # binary/dichotomic search on lists
from PIL import Image
import util
try:
    from tqdm import tqdm
except ImportError:  # optional dependency, simply print a X/Y ratio on each step else
    def tqdm(iterable, total):  # fallback
        for j, _ in enumerate(iterable):
            if j % 100 == 0:
                yield ''  # print(f'{j} / {total}')


def run(source_image, palette_image):
    print(util.timestamp() + ' Applying filter: Steal colors with same brightness')

    tokens = source_image.split('.')
    destination_image = tokens[0] + '_colorstolen.' + tokens[1]

    img = Image.open(source_image)

    steal_colors(img, palette_image)
    img.save(destination_image)

    return destination_image


def steal_colors(img, palette_img_src):
    print('# Building replacement palette')
    palette = Palette(palette_img_src, brightness_func=luminosity)

    print('# Subsituting colors')
    img_height = img.size[1]
    list(tqdm(subst_img_colors(img, palette, brightness_func=luminosity), total=img_height))


class Palette:
    def __init__(self, palette_img_src, brightness_func):
        self.palette = {}
        with Image.open(palette_img_src) as palette_img:
            palette_img_height = palette_img.size[1]
            list(tqdm(self._build_palette(palette_img, brightness_func), total=palette_img_height))
        self.sorted_keys = sorted(self.palette.keys())

    def _build_palette(self, palette_img, brightness_func):
        width, height = palette_img.size
        palette_pixels = palette_img.load()  # getting PixelAccess
        for j in range(height):
            for i in range(width):
                brightness = brightness_func(palette_pixels[i, j])
                # nothing smart (ex: avg): we only keep the last brightness value processed
                self.palette[brightness] = palette_pixels[i, j]
            yield 'ROW_COMPLETE'  # progress tracking

    def __getitem__(self, key):
        i = bisect_left(self.sorted_keys, key)  # O(logN)
        return self.palette[self.sorted_keys[i]]


def subst_img_colors(img, luminosity2color_palette, brightness_func):
    width, height = img.size
    img = img.load()  # getting PixelAccess
    for j in range(height):
        for i in range(width):
            img[i, j] = luminosity2color_palette[brightness_func(img[i, j])]
        yield 'ROW_COMPLETE'  # progress tracking


def luminosity(pixel):
    r, g, b = pixel
    return 0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2)
