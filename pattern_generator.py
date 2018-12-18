from os import listdir, path
from io import open
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap
from unidecode import unidecode
import util


__author__ = 'Ziga Vucko'


SIZE = (0, 0)
N_COLS = [2, 3, 4, 5, 6, 7]
MAX_BLANKS = 5
TYPEFACES = {
    'background': ['Times New Roman', 'Garamond'],
    'overlay': ['Helvetica Bold', 'Impact'],
    'serial-number': 'Impact'
}
FONT_SIZES = {
    'background': 35,
    'overlay-twitter': {
        'Times New Roman': 140,
        'Garamond': 140,
        'Helvetica Bold': 140,
        'Impact': 150
    },
    'overlay-quote': {
        'Times New Roman': 150,
        'Garamond': 150,
        'Helvetica Bold': 150,
        'Impact': 165
    },
    'serial-number': 70
}


def load_font(typeface, font_size):
    return ImageFont.truetype('fonts/' + typeface + '.ttf', font_size)


def load_cache_text(keyword, type):
    return unidecode(open('cache/' + keyword + '/text/' + type + '.txt', 'r', encoding='utf_8').read())


def load_data_text(file_name, type):
    return unidecode(open('data/text/' + type + '/' + file_name, 'r', encoding='iso8859_2').read())


def load_cache_image(keyword, file_name):
    return Image.open('cache/' + keyword + '/images/' + file_name)


def get_overlay_text_lines(text, line_chars=30):
    split_lines = text.replace('\n\n\n', '\n').replace('\n\n', '\n').splitlines()
    lines = []
    for line in split_lines:
        lines += textwrap.wrap(line, width=line_chars) + ['\n']
    return lines


def get_cache_overlay_text_lines(text, line_chars=30):
    lines = text.replace('\n\n\n', '\n').replace('\n\n', '\n').splitlines()
    if len(lines) > 0:
        line = lines[np.argmax(list(map(lambda l: len(l), lines)))]
        return textwrap.wrap(line, width=line_chars)
    else:
        return []


def get_data_overlay_text_lines(text, line_chars=30):
    return textwrap.wrap(text, width=line_chars)


def build_text_canvas(lines, font, width, height, align='left', angle=0, transparent=False):
    mode = 'RGB'
    background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    if transparent:
        mode = 'RGBA'
        background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 0)

    canvas = Image.new(mode, (width, round(height * 1.5)), background_color)
    draw = ImageDraw.Draw(canvas)
    text = '\n'.join(lines) if len(lines) > 1 else lines[0]
    fill_color = '#%02X%02X%02X' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    draw.multiline_text((0, 0), text, font=font, fill=fill_color, align=align)
    return canvas.rotate(angle=angle, expand=True) if angle is not 0 else canvas


def generate_images(keywords):
    random.shuffle(keywords)
    images = []

    # Load images from the cache.
    for keyword in keywords:
        for file in listdir('cache/' + keyword + '/images/'):
            try:
                img_cache = load_cache_image(keyword, file)
                images.append(img_cache)
            except OSError:
                pass

    random.shuffle(images)

    return images


def generate_overlay_text(keywords, typeface):
    random.shuffle(keywords)

    # Randomly choose the number of columns of overlay text.
    n_cols = random.choice(N_COLS)
    print('\t\tNumber of overlay text columns:', n_cols)

    font = load_font(typeface, font_size=FONT_SIZES['background'])
    char_width, char_height = font.getsize('a')
    column_separator_width = char_width
    column_width = int(np.floor((SIZE[0] - ((n_cols - 1) * column_separator_width)) / n_cols))
    column_width = round(column_width * 1.025)
    column_chars = int(np.floor(column_width / char_width))
    column_lines = int(np.ceil(SIZE[1] / char_height))
    column_height = char_height * column_lines

    lines = []

    # Format text lines from the randomly chosen long data texts.
    files = listdir('data/text/long')
    random.shuffle(files)
    unused_files = list(files)

    # Format text lines from Wikipedia cache text.
    for keyword in keywords:
        if path.exists('cache/' + keyword + '/text/wikipedia.txt') and len(lines) < n_cols * column_lines:
            lines += get_overlay_text_lines(text=load_cache_text(keywords[0], 'wikipedia'), line_chars=column_chars)

            # Append random number of new lines (blank space).
            lines += random.randint(0, MAX_BLANKS) * ['\n']

    # Format text lines from the randomly chosen long data texts (if necessary).
    i = 0
    while len(lines) < n_cols * column_lines and i < len(unused_files):
        lines += get_overlay_text_lines(text=load_data_text(unused_files[i], 'long'), line_chars=column_chars)

        # Append random number of new lines (blank space).
        lines += random.randint(0, MAX_BLANKS) * ['\n']

        i += 1

    # Use formatted text lines to build column canvases.
    canvases = []
    for i in range(n_cols):
        text = build_text_canvas(lines[i * column_lines:(i + 1) * column_lines], font, column_width, column_height,
                                 transparent=True)
        x = i * column_width
        if n_cols > 1:
            x += i * column_separator_width
        canvases.append({'text': text, 'position': (x, 0)})

    return canvases


def generate_twitter_overlay_text(keywords, typeface):
    keyword = random.choice(keywords)

    font = load_font(typeface, font_size=FONT_SIZES['overlay-twitter'][typeface])
    char_height = font.getsize('a')[1]
    max_chars = 25

    if random.random() < 0.5:
        # Format a text line from Twitter cache text using just the longest tweet.
        # Iterate because some 'twitter.txt' files might be empty (no tweets exist for the given keyword).
        n_lines = 0
        while n_lines is 0:
            lines = get_cache_overlay_text_lines(text=load_cache_text(keyword, 'twitter'), line_chars=max_chars)
            n_lines = len(lines)
            keyword = random.choice(keywords)
        text_width = round(font.getsize(lines[np.argmax(list(map(lambda l: len(l), lines)))])[0] * 1.15)
        text_height = n_lines * char_height
    else:
        # Format a text line from a random long data text.
        files = listdir('data/text/short')
        random.shuffle(files)
        lines = get_data_overlay_text_lines(text=load_data_text(files[0], 'short'), line_chars=max_chars)
        text_width = round(font.getsize(lines[np.argmax(list(map(lambda l: len(l), lines)))])[0] * 1.15)
        text_height = len(lines) * char_height

    # Use formatted text line to build the canvas.
    return build_text_canvas(lines, font, text_width, text_height, align='right', transparent=True)


def generate_serial_number(serial_number):
    font = load_font(TYPEFACES['serial-number'], font_size=FONT_SIZES['serial-number'])
    char_height = font.getsize('a')[1]

    # Format a text line representing the serial number of the document.
    lines = ['Serial No %05d' % serial_number]
    text_width = font.getsize(lines[0])[0]
    text_height = char_height

    # Use formatted text line to build the canvas.
    return build_text_canvas(lines, font, text_width, text_height, transparent=True)


def run(file, width, height, keywords, serial_number):
    global SIZE

    print(util.timestamp() + ' Generating a pattern (%d x %d) with serial #%d from keywords: %s' %
          (width, height, serial_number, ', '.join(keywords)))

    SIZE = (width, height)
    keywords = list(map(lambda k: k.lower().replace(' ', ''), keywords))

    # Randomly choose the typefaces.
    background_typeface = random.choice(TYPEFACES['background'])
    overlay_typeface = random.choice(TYPEFACES['overlay'])
    print('\t\tFonts: %s, %s' % (background_typeface, overlay_typeface))

    # Create a blank canvas.
    canvas = Image.new('RGB', SIZE, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # Draw images on the blank canvas.
    images = generate_images(keywords)
    one_tenth_width, one_tenth_height = round(SIZE[0] * 0.1), round(SIZE[1] * 0.1)
    for i, image in enumerate(images):
        width, height = image.size
        a = SIZE[0] - width + one_tenth_width
        b = SIZE[1] - height + one_tenth_height
        position = (random.randint(-one_tenth_width, max(a, 0)),
                    random.randint(-one_tenth_height, max(b, 0)))
        canvas.paste(image, position)

    # Draw the Wikipedia overlay text.
    overlay_text_canvases = generate_overlay_text(keywords, background_typeface)
    for column_text_canvas in overlay_text_canvases:
        canvas.paste(column_text_canvas['text'], column_text_canvas['position'], mask=column_text_canvas['text'])

    # Draw the Twitter overlay text.
    twitter_overlay_text_canvas = generate_twitter_overlay_text(keywords, overlay_typeface)
    text_width, text_height = twitter_overlay_text_canvas.size
    twitter_pos = {
        'x': random.randint(0, max(SIZE[0] - text_width, 0)),
        'y': random.randint(0, max(SIZE[1] - text_height, 0)),
        'width': text_width,
        'height': text_height
    }
    canvas.paste(twitter_overlay_text_canvas, (twitter_pos['x'], twitter_pos['y']),
                 mask=twitter_overlay_text_canvas)

    # Draw the serial number overlay text.
    serial_number_text_canvas = generate_serial_number(serial_number)
    text_width, text_height = serial_number_text_canvas.size
    serial_number_pos = {
        'x': round(SIZE[0] - 1.1 * text_width),
        'y': round(SIZE[1] - 1.1 * text_height),
        'width': text_width,
        'height': text_height
    }
    canvas.paste(serial_number_text_canvas, (serial_number_pos['x'], serial_number_pos['y']),
                 mask=serial_number_text_canvas)

    # Save the canvas to an image file.
    canvas.save(file)
