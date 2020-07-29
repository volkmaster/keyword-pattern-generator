import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSlot
from api import api_caller
from filtering import elastic_transform, japanify, pixelsort, smoothing, ripple_effect, segmentation
import pattern_generator
import util


__author__ = 'Ziga Vucko'


FILTERS = ['Elastic transform (liquify)', 'Japanify', 'Pixel sorting', 'Smoothing', 'Ripple effect', 'Segmentation']
FILTER_PARAMETERS = [('Alpha', '10000'), ('Density', '50'), ('Sorting path', 'diagonal'), ('Kernel size', '10'), ('K', '5'), ('Weight', '29')]

PIXEL_SORTING_ALLOWED_PARAMETERS = [
    'angled-line',
    'circles',
    'concentric',
    'diagonal',
    'diagonal-single',
    'fill-circles',
    'horizontal',
    # 'random-walk',
    # 'random-walk-horizontal',
    # 'random-walk-vertical',
    'vertical'
]

PIXEL_SORTING_PARAMETERS_HELP = [
    ('angled-line,[angle=0]', 'Sort pixels in lines tilted at the given angle.'),
    ('circles', 'Pixels are sorted in concentric circles about the center of the image.'),
    ('concentric', 'Pixels are sorted in concentric rectangles.'),
    ('diagonal', 'Pixels are sorted in diagonal lines.'),
    ('diagonal-single', 'Pixels sorted in a single path that moves diagonally through the image.'),
    ('fill-circles,[radius=100]', 'Covers the image in circles of the given radius.'),
    ('horizontal', 'Pixels sorted horizontally.'),
    # ('random-walk', 'Pixels sorted in random walks over the image.'),
    # ('random-walk-horizontal', 'Pixels sorted in random walks moving horizontally over the image.'),
    # ('random-walk-vertical', 'Pixels sorted in random walks moving vertically over the image.'),
    ('vertical', 'Pixels sorted vertically.')
]


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Keyword Pattern Generator'
        self.width = 850
        self.height = 420

        self.label_title_keywords = None
        self.textboxes_keywords = [None, None, None, None, None]

        self.label_title_filters = None
        self.textboxes_numbers_filters = [None for _ in FILTERS]
        self.labels_filters = [None for _ in FILTERS]
        self.labels_parameters_filters = [None for _ in FILTERS]
        self.textboxes_parameters_filters = [None for _ in FILTERS]
        self.button_help_pixel_sorting = None

        self.button_generate = None

        self.label_width = None
        self.textbox_width = None
        self.label_height = None
        self.textbox_height = None

        self.label_status = None

        with open('serial_number.txt', 'r') as file:
            self.serial_no = int(file.read())

        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.move(QApplication.desktop().availableGeometry().center() - self.frameGeometry().center())

        # Create a title label for keywords
        self.label_title_keywords = QLabel('Enter up to 5 keywords:', self)
        self.label_title_keywords.move(25, 10)
        self.label_title_keywords.resize(250, 30)

        # Create textboxes for keywords
        for i in range(len(self.textboxes_keywords)):
            self.textboxes_keywords[i] = QLineEdit(self)
            self.textboxes_keywords[i].move(25, 10 + (i + 1) * 40)
            self.textboxes_keywords[i].resize(250, 30)
            self.textboxes_keywords[i].textChanged.connect(self.on_keyword_change)

        # Create a title label for filters
        self.label_title_keywords = QLabel(f'Order filters (1-{len(FILTERS)} / empty) and fill out parameters:', self)
        self.label_title_keywords.move(325, 10)
        self.label_title_keywords.resize(300, 30)

        # Create textboxes for filters (numbers)
        for i in range(len(self.textboxes_numbers_filters)):
            self.textboxes_numbers_filters[i] = QLineEdit(self)
            self.textboxes_numbers_filters[i].move(325, 10 + (i + 1) * 40)
            self.textboxes_numbers_filters[i].resize(30, 30)

        # Create labels for filters
        for i in range(len(self.labels_filters)):
            self.labels_filters[i] = QLabel(FILTERS[i], self)
            self.labels_filters[i].move(365, 10 + (i + 1) * 40)
            self.labels_filters[i].resize(165, 30)

        # Create labels for filters (parameters)
        for i in range(len(self.labels_filters)):
            self.labels_parameters_filters[i] = QLabel(FILTER_PARAMETERS[i][0], self)
            self.labels_parameters_filters[i].move(530, 10 + (i + 1) * 40)
            self.labels_parameters_filters[i].resize(80, 30)

        # Create textboxes for filters (parameters)
        for i in range(len(self.textboxes_numbers_filters)):
            self.textboxes_parameters_filters[i] = QLineEdit(FILTER_PARAMETERS[i][1], self)
            self.textboxes_parameters_filters[i].move(620, 10 + (i + 1) * 40)
            self.textboxes_parameters_filters[i].resize(160, 30)

            if FILTERS[i] == 'Pixel sorting':
                self.button_help_pixel_sorting = QPushButton('Help', self)
                self.button_help_pixel_sorting.move(790, 10 + (i + 1) * 40)
                self.button_help_pixel_sorting.resize(40, 30)
                self.button_help_pixel_sorting.clicked.connect(self.on_help_pixel_sorting)

        # Create a button for pattern generation
        self.button_generate = QPushButton('Generate pattern', self)
        self.button_generate.move(75, 265)
        self.button_generate.resize(150, 50)
        self.button_generate.setEnabled(False)
        self.button_generate.clicked.connect(self.on_generate_pattern)

        # Create a width label
        self.label_width = QLabel('Width of pattern (in px):', self)
        self.label_width.move(325, 315)
        self.label_width.resize(150, 30)

        # Create a width textbox
        self.textbox_width = QLineEdit('1000', self)
        self.textbox_width.move(485, 315)
        self.textbox_width.resize(70, 30)

        # Create a height label
        self.label_height = QLabel('Height of pattern (in px):', self)
        self.label_height.move(325, 355)
        self.label_height.resize(150, 30)

        # Create a height textbox
        self.textbox_height = QLineEdit('1000', self)
        self.textbox_height.move(485, 355)
        self.textbox_height.resize(70, 30)

        # Create a status label
        self.label_status = QLabel(self)
        self.label_status.move(25, 340)
        self.label_status.resize(550, 60)
        self.label_status.setWordWrap(True)

        self.show()

    @pyqtSlot()
    def on_keyword_change(self):
        keywords = [textbox.text() for textbox in self.textboxes_keywords if textbox.text() is not '']
        self.button_generate.setEnabled(len(keywords) > 0)

        self.label_status.setText('')

    @pyqtSlot()
    def on_help_pixel_sorting(self):
        dialog = QDialog()
        dialog.setWindowTitle('Pixel sorting: sorting path parameter help')
        dialog.setFixedSize(700, 2 * 20 + len(PIXEL_SORTING_PARAMETERS_HELP) * 30)

        for i, (name, label_description) in enumerate(PIXEL_SORTING_PARAMETERS_HELP):
            label_name = QLabel(name, dialog)
            label_name.move(20, 20 + i * 30)
            label_name.resize(200, 20)

            label_description = QLabel(label_description, dialog)
            label_description.move(230, 20 + i * 30)
            label_description.resize(450, 20)

        dialog.exec_()

    @pyqtSlot()
    def on_generate_pattern(self):
        self.before_generate_pattern()

        file = 'images/pattern.png'

        keywords = [textbox.text().strip() for textbox in self.textboxes_keywords if textbox.text() is not '']

        for keyword in keywords:
            try:
                api_caller.run(keyword)
            except util.Error as e:
                self.label_status.setText(e.message())
                self.after_generate_pattern()
                return

        width = int(self.textbox_width.text())
        height = int(self.textbox_height.text())

        pattern_generator.run(file, width, height, keywords, self.serial_no)

        filters = []
        for i in range(len(FILTERS)):
            text_number = self.textboxes_numbers_filters[i].text()
            text_parameter = self.textboxes_parameters_filters[i].text()
            if text_number and text_parameter:
                filters.append((i, int(text_number), text_parameter))

        filters.sort(key=lambda x: x[1])
        for (i, number, parameter) in filters:
            # Elastic transform (liquify)
            if i == 0:
                file = elastic_transform.run(file, alpha=int(parameter), sigma=8)
            # Japanify
            elif i == 1:
                file = japanify.run(file, density=int(parameter))
            # Pixel sorting
            elif i == 2:
                tokens = parameter.split(',')
                if tokens[0] not in PIXEL_SORTING_ALLOWED_PARAMETERS:
                    self.label_status.setText('Pixel sorting parameter is not allowed or not formatted properly. ' +
                                              'Check help.')
                    self.after_generate_pattern()
                    return
                value = '' if len(tokens) == 1 else tokens[1]
                file = pixelsort.run(file, sorting_path=tokens[0], value=value)
            # Smoothing
            elif i == 3:
                file = smoothing.run(file, kernel_size=int(parameter))
            # Ripple effect
            elif i == 4:
                file = ripple_effect.run(file, k=int(parameter))
            # Segmentation
            elif i == 5:
                file = segmentation.run(file, weight=int(parameter))

        status = ['Pattern with serial number #' + str(self.serial_no) + ' successfully generated.',
                  'Filters applied: ' + ', '.join([FILTERS[i] for (i, _, _) in filters])]
        self.label_status.setText(status[0] + '\n' + status[1])
        print(util.timestamp() + ' ' + ' '.join(status) + '\n')

        self.increment_serial_no()

        self.after_generate_pattern()

    def before_generate_pattern(self):
        for textbox in self.textboxes_keywords:
            textbox.setEnabled(False)

        for textbox in self.textboxes_numbers_filters:
            textbox.setEnabled(False)

        for textbox in self.textboxes_parameters_filters:
            textbox.setEnabled(False)

        self.button_help_pixel_sorting.setEnabled(False)

        self.textbox_width.setEnabled(False)
        self.textbox_height.setEnabled(False)

        self.button_generate.setEnabled(False)

        self.label_status.setText('')

    def after_generate_pattern(self):
        for textbox in self.textboxes_keywords:
            textbox.setEnabled(True)

        for textbox in self.textboxes_numbers_filters:
            textbox.setEnabled(True)

        for textbox in self.textboxes_parameters_filters:
            textbox.setEnabled(True)

        self.button_help_pixel_sorting.setEnabled(True)

        self.textbox_width.setEnabled(True)
        self.textbox_height.setEnabled(True)

        self.button_generate.setEnabled(True)

    def increment_serial_no(self):
        self.serial_no += 1

        with open('serial_number.txt', 'w') as file:
            file.write(str(self.serial_no))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
