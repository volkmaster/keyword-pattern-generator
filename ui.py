import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSlot
import api_caller
import document_generator
import util


__author__ = 'Ziga Vucko'


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Keyword Document Generator'
        self.width = 300
        self.height = 300
        self.label_title = None
        self.label_status = None
        self.textboxes = [None, None, None]
        self.button = None

        with open('serial_number.txt', 'r') as file:
            self.serial_no = int(file.read())

        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.move(QApplication.desktop().availableGeometry().center() - self.frameGeometry().center())

        # Create a title label
        self.label_title = QLabel('Enter up to 3 keywords:', self)
        self.label_title.move(25, 10)
        self.label_title.resize(250, 30)

        # Create textboxes for keywords
        for i in range(len(self.textboxes)):
            self.textboxes[i] = QLineEdit(self)
            self.textboxes[i].move(25, 10 + (i + 1) * 40)
            self.textboxes[i].resize(250, 30)
            self.textboxes[i].textChanged.connect(self.on_keyword_change)

        # Create a button for document generation
        self.button = QPushButton('Generate document', self)
        self.button.move(75, 185)
        self.button.resize(150, 50)
        self.button.setEnabled(False)
        self.button.clicked.connect(self.on_generate_document)

        # Create a status label
        self.label_status = QLabel('', self)
        self.label_status.move(25, 240)
        self.label_status.resize(250, 60)
        self.label_status.setWordWrap(True)

        self.show()

    @pyqtSlot()
    def on_keyword_change(self):
        keywords = [textbox.text() for textbox in self.textboxes if textbox.text() is not '']
        self.button.setEnabled(len(keywords) > 0)

        self.label_status.setText('')

    @pyqtSlot()
    def on_generate_document(self):
        self.before_generate_document()

        keywords = [textbox.text() for textbox in self.textboxes if textbox.text() is not '']

        for keyword in keywords:
            try:
                api_caller.run(keyword)
            except util.Error as e:
                self.label_status.setText(e.message())
                self.after_generate_document()
                return

        document_generator.run(keywords, self.serial_no)

        self.label_status.setText('Document with serial number #' + str(self.serial_no) + ' successfully generated.')
        self.increment_serial_no()

        self.after_generate_document()

    def before_generate_document(self):
        for textbox in self.textboxes:
            textbox.setEnabled(False)

        self.button.setEnabled(False)

        self.label_status.setText('')

    def after_generate_document(self):
        for textbox in self.textboxes:
            textbox.setEnabled(True)

        self.button.setEnabled(True)

    def increment_serial_no(self):
        self.serial_no += 1

        with open('serial_number.txt', 'w') as file:
            file.write(str(self.serial_no))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
