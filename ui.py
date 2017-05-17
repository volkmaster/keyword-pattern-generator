import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSlot, QTimer
import api_caller

__author__ = 'Ziga Vucko'


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Brand New Coexistence BNC'
        self.width = 400
        self.height = 70
        self.textbox = None
        self.button = None

        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.move(QApplication.desktop().availableGeometry().center() - self.frameGeometry().center())

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText('Enter keyword...')
        self.textbox.move(20, 20)
        self.textbox.resize(250, 30)

        # Create a button in the window
        self.button = QPushButton('Print', self)
        self.button.move(290, 14)
        self.button.resize(95, 45)

        # Connect button to on click event handler
        self.button.clicked.connect(self.on_print)

        self.show()

    @pyqtSlot()
    def on_print(self):
        text = self.textbox.text()
        reply = QMessageBox.question(self, text, 'Do you want to create and print documents for keyword "' + text + '"?',
                                     QMessageBox.Cancel, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.before_print()

            # Call the APIs, prepare documents and print them.
            api_caller.run(text)

            self.after_print()

    def before_print(self):
        self.textbox.setText('')
        self.textbox.setPlaceholderText('Please wait...')
        self.textbox.setEnabled(False)

        self.button.setText('Printing')
        self.button.setEnabled(False)

    def after_print(self):
        self.textbox.setPlaceholderText('Enter keyword...')
        self.textbox.setEnabled(True)

        self.button.setText('Print')
        self.button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
