from os import listdir
from io import open
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap
from unidecode import unidecode
import util
import settings


__author__ = 'Ziga Vucko'


A4_SIZE = (2480, 3508)
N_COLS = [2, 3, 4]
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


def load_data_image(file_name):
    return Image.open('data/images/' + file_name)


def get_background_text_lines(text, line_chars=30):
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
    color = (255, 255, 255)
    if transparent:
        mode = 'RGBA'
        color = (255, 255, 255, 0)

    canvas = Image.new(mode, (width, round(height * 1.5)), color)
    draw = ImageDraw.Draw(canvas)
    text = '\n'.join(lines) if len(lines) > 1 else lines[0]
    draw.multiline_text((0, 0), text, font=font, fill="#000000", align=align)
    return canvas.rotate(angle=angle, expand=True) if angle is not 0 else canvas


def generate_background_text(keywords, typeface):
    random.shuffle(keywords)

    # Randomly choose the number of columns of background text.
    n_cols = random.choice(N_COLS)
    print('\t\tNumber of background columns:', n_cols)

    font = load_font(typeface, font_size=FONT_SIZES['background'])
    char_width, char_height = font.getsize('a')
    column_separator_width = char_width
    column_width = int(np.floor((A4_SIZE[0] - ((n_cols - 1) * column_separator_width)) / n_cols))
    column_width = round(column_width * 1.025)
    column_chars = int(np.floor(column_width / char_width))
    column_lines = int(np.ceil(A4_SIZE[1] / char_height))
    column_height = char_height * column_lines

    lines = []

    files = listdir('data/text/long')
    random.shuffle(files)
    unused_files = list(files)

    # Format text lines from the randomly chosen long data texts.
    i = 0
    while len(lines) < n_cols * column_lines and i < len(files):
        lines += get_background_text_lines(text=load_data_text(files[i], 'long'), line_chars=column_chars)

        # Append random number of new lines (blank space).
        lines += random.randint(0, MAX_BLANKS) * ['\n']

        unused_files.remove(files[i])
        i += 1
        if random.random() < 0.3:
            break

    # Format text lines from Wikipedia cache text.
    if len(lines) < n_cols * column_lines:
        lines += get_background_text_lines(text=load_cache_text(keywords[0], 'wikipedia'), line_chars=column_chars)

        # Append random number of new lines (blank space).
        lines += random.randint(0, MAX_BLANKS) * ['\n']

    # Format text lines from the randomly chosen long data texts (if necessary).
    i = 0
    while len(lines) < n_cols * column_lines and i < len(unused_files):
        lines += get_background_text_lines(text=load_data_text(unused_files[i], 'long'), line_chars=column_chars)

        # Append random number of new lines (blank space).
        lines += random.randint(0, MAX_BLANKS) * ['\n']

        i += 1

    # Use formatted text lines to build column canvases.
    canvases = []
    for i in range(n_cols):
        text = build_text_canvas(lines[i * column_lines:(i + 1) * column_lines], font, column_width, column_height)
        x = i * column_width
        if n_cols > 1:
            x += i * column_separator_width
        canvases.append({'text': text, 'position': (x, 0)})

    return canvases


def generate_images(keywords):
    keyword = random.choice(keywords)
    images = []

    # Randomly select two images from the cache.
    files = listdir('cache/' + keyword + '/images/')
    random.shuffle(files)
    for file_name in files[:2]:
        img_cache = load_cache_image(keyword, file_name)
        images.append(img_cache)

    # Randomly select two images from the data.
    files = listdir('data/images')
    random.shuffle(files)
    for file_name in files[:3]:
        img_data = load_data_image(file_name)
        width, height = img_data.size
        img_data = img_data.resize((round(1.5 * width), round(1.5 * height)), Image.ANTIALIAS)
        images.append(img_data)

    # Sort images by size in descending order.
    images.sort(key=lambda img: img.size[0] * img.size[1], reverse=True)

    # Resize the largest image (so that we have at least one very large image).
    width, height = images[0].size
    images[0] = images[0].resize((1500, round(height * (1500. / width))), Image.ANTIALIAS)

    return images


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


def generate_quote_overlay_text(typeface):
    font = load_font(typeface, font_size=FONT_SIZES['overlay-quote'][typeface])
    char_height = font.getsize('-')[1]
    max_chars = 50

    # Format a text line from one of the data texts that is maximally 50 characters long.
    lines = []

    files = listdir('data/text/short')
    random.shuffle(files)
    for file_name in files:
        text = load_data_text(file_name, 'short')
        if len(text) <= max_chars:
            lines = [text]
            break

    text_width = font.getsize(lines[0])[0]
    text_height = char_height

    # Use formatted text line to build the canvas.
    return build_text_canvas(lines, font, text_width, text_height, angle=90, transparent=True)


def generate_serial_number(serial_number):
    font = load_font(TYPEFACES['serial-number'], font_size=FONT_SIZES['serial-number'])
    char_height = font.getsize('a')[1]

    # Format a text line representing the serial number of the document.
    lines = ['BNC Print No %05d' % serial_number]
    text_width = font.getsize(lines[0])[0]
    text_height = char_height

    # Use formatted text line to build the canvas.
    return build_text_canvas(lines, font, text_width, text_height, transparent=True)


def run(keywords, serial_number):
    print(util.timestamp() + ' Generating a document with serial #' + str(serial_number) + ' from keywords: ' + str(keywords[:3]))

    keywords = list(map(lambda k: k.lower().replace(' ', ''), keywords))

    # Randomly choose the typefaces.
    background_typeface = random.choice(TYPEFACES['background'])
    overlay_typeface = random.choice(TYPEFACES['overlay'])
    print('\t\tBackground font:', background_typeface)
    print('\t\tOverlay font:', overlay_typeface)

    # Create a blank white canvas.
    canvas = Image.new('RGB', A4_SIZE, (255, 255, 255))

    # Draw the text background text columns.
    background_text_canvases = generate_background_text(keywords, background_typeface)
    for column_text_canvas in background_text_canvases:
        canvas.paste(column_text_canvas['text'], column_text_canvas['position'])

    # Draw images on top of the background text.
    positions = [
        [(150, 200), (800, 200), (1600, 200)],
        [(400, 600), (900, 600), (1500, 600)],
        [(250, 1400), (700, 1400), (1400, 1400)],
        [(200, 2000), (1000, 2000), (1550, 2000)],
        [(320, 2600), (850, 2600), (1450, 2600)]
    ]
    random.shuffle(positions)

    images = generate_images(keywords)
    curr, prev = 0, 0
    for i, img in enumerate(images):
        while curr is prev:
            curr = random.randint(0, 2)
        canvas.paste(img, positions[i][curr])
        prev = curr

    # Draw the Twitter overlay text.
    twitter_overlay_text_canvas = generate_twitter_overlay_text(keywords, overlay_typeface)
    text_width, text_height = twitter_overlay_text_canvas.size
    twitter_pos = {
        'x': random.randint(0, A4_SIZE[0] - text_width),
        'y': random.randint(0, A4_SIZE[1] - text_height),
        'width': text_width,
        'height': text_height
    }
    canvas.paste(twitter_overlay_text_canvas, (twitter_pos['x'], twitter_pos['y']), mask=twitter_overlay_text_canvas)

    # Draw the vertical quote overlay text.
    quote_overlay_text_canvas = generate_quote_overlay_text(overlay_typeface)
    text_width, text_height = quote_overlay_text_canvas.size
    quote_pos = {
        'x': 0,
        'y': 0,
        'width': text_width,
        'height': text_height
    }
    left_diff = twitter_pos['x']
    right_diff = A4_SIZE[0] - (twitter_pos['x'] + twitter_pos['width'])
    start_left = 0
    end_left = twitter_pos['x'] - quote_pos['width']
    start_right = twitter_pos['x'] + twitter_pos['width']
    end_right = A4_SIZE[0] - quote_pos['width']
    if left_diff >= right_diff and end_left >= 0:
        quote_pos['x'] = random.randint(start_left, end_left)
        quote_pos['y'] = random.randint(0, A4_SIZE[1] - quote_pos['height'])
    elif start_right <= end_right:
        quote_pos['x'] = random.randint(start_right, end_right)
        quote_pos['y'] = random.randint(0, A4_SIZE[1] - quote_pos['height'])
    else:
        quote_pos['x'] = random.randint(0, A4_SIZE[0])
        quote_pos['y'] = random.randint(0, A4_SIZE[1])
    canvas.paste(quote_overlay_text_canvas, (quote_pos['x'], quote_pos['y']), mask=quote_overlay_text_canvas)

    # Draw the serial number overlay text.
    serial_number_text_canvas = generate_serial_number(serial_number)
    text_width, text_height = serial_number_text_canvas.size
    serial_number_pos = {
        'x': round(A4_SIZE[0] - 1.1 * text_width),
        'y': round(A4_SIZE[1] * 0.965),
        'width': text_width,
        'height': text_height
    }
    canvas.paste(serial_number_text_canvas, (serial_number_pos['x'], serial_number_pos['y']), mask=serial_number_text_canvas)

    # Save the canvas to an image file.
    canvas.save(settings.DOCUMENT_NAME, 'png')
