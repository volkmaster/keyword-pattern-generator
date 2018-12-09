import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSlot
from api import api_caller
from filtering import elastic_transform, japanify, pixelsort, smoothing, ripple_effect
import pattern_generator
import util


__author__ = 'Ziga Vucko'


FILTERS = ['Elastic transform (liquify)', 'Japanify', 'Pixel sorting', 'Smoothing', 'Ripple effect']


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Keyword Pattern Generator'
        self.width = 600
        self.height = 380

        self.label_title_keywords = None
        self.textboxes_keywords = [None, None, None, None, None]

        self.label_title_filters = None
        self.textboxes_filters = [None for _ in FILTERS]
        self.labels_filters = [None for _ in FILTERS]

        self.button_generate = None

        self.label_size = None
        self.textbox_size = None

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
        self.label_title_keywords = QLabel('Order filters (1-5 / empty):', self)
        self.label_title_keywords.move(325, 10)
        self.label_title_keywords.resize(250, 30)

        # Create textboxes for filters
        for i in range(len(self.textboxes_filters)):
            self.textboxes_filters[i] = QLineEdit(self)
            self.textboxes_filters[i].move(325, 10 + (i + 1) * 40)
            self.textboxes_filters[i].resize(30, 30)

        # Create labels for filters
        for i in range(len(self.labels_filters)):
            self.labels_filters[i] = QLabel(FILTERS[i], self)
            self.labels_filters[i].move(365, 10 + (i + 1) * 40)
            self.labels_filters[i].resize(250, 30)

        # Create a button for pattern generation
        self.button_generate = QPushButton('Generate pattern', self)
        self.button_generate.move(75, 265)
        self.button_generate.resize(150, 50)
        self.button_generate.setEnabled(False)
        self.button_generate.clicked.connect(self.on_generate_pattern)

        # Create a size label
        self.label_size = QLabel('Size of pattern (in px):', self)
        self.label_size.move(325, 275)
        self.label_size.resize(150, 30)

        # Create a size textbox
        self.textbox_size = QLineEdit(self)
        self.textbox_size.move(485, 275)
        self.textbox_size.resize(70, 30)
        self.textbox_size.setText('1000')

        # Create a status label
        self.label_status = QLabel('', self)
        self.label_status.move(25, 320)
        self.label_status.resize(550, 60)
        self.label_status.setWordWrap(True)

        self.show()

    @pyqtSlot()
    def on_keyword_change(self):
        keywords = [textbox.text() for textbox in self.textboxes_keywords if textbox.text() is not '']
        self.button_generate.setEnabled(len(keywords) > 0)

        self.label_status.setText('')

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

        size = int(self.textbox_size.text())

        pattern_generator.run(file, size, keywords, self.serial_no)

        filters = []
        for i, textbox in enumerate(self.textboxes_filters):
            text = textbox.text()
            if text:
                filters.append((int(text), i))

        filters.sort(key=lambda x: x[0])
        for (index, i) in filters:
            # Elastic transform (liquify)
            if i == 0:
                file = elastic_transform.run(file, alpha=2000, sigma=8)
            # Japanify
            elif i == 1:
                file = japanify.run(file, density=75)
            # Pixel sorting
            elif i == 2:
                file = pixelsort.run(file)
            # Smoothing
            elif i == 3:
                file = smoothing.run(file, kernel_size=10)
            # Ripple effect
            elif i == 4:
                file = ripple_effect.run(file, k=10)

        status = ['Pattern with serial number #' + str(self.serial_no) + ' successfully generated.',
                  'Filters applied: ' + ', '.join([FILTERS[i] for _, i in filters])]
        self.label_status.setText(status[0] + '\n' + status[1])
        print(util.timestamp() + ' ' + ' '.join(status) + '\n')

        self.increment_serial_no()

        self.after_generate_pattern()

    def before_generate_pattern(self):
        for textbox in self.textboxes_keywords:
            textbox.setEnabled(False)

        for textbox in self.textboxes_filters:
            textbox.setEnabled(False)

        self.textbox_size.setEnabled(False)

        self.button_generate.setEnabled(False)

        self.label_status.setText('')

    def after_generate_pattern(self):
        for textbox in self.textboxes_keywords:
            textbox.setEnabled(True)

        for textbox in self.textboxes_filters:
            textbox.setEnabled(True)

        self.textbox_size.setEnabled(True)

        self.button_generate.setEnabled(True)

    def increment_serial_no(self):
        self.serial_no += 1

        with open('serial_number.txt', 'w') as file:
            file.write(str(self.serial_no))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
