import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QLineEdit, QPushButton

class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.Program()
        self.Title()
        self.Detail()
        self.Button()
        self.show()

    def Program(self):
        self.setWindowTitle('Account Registration')
        self.setGeometry(100, 100, 400, 400)

    def Title(self):
        self.title_label = QLabel('Account Registration System', self)
        self.title_label.move(100, 20)

    def Detail(self):
        self.fields = ['First Name', 'Last Name', 'Username', 'Password', 'Email Address', 'Contact Number']
        self.y_position = 60
        self.text_fields = []
        for field in self.fields:
            label = QLabel(field, self)
            label.move(50, self.y_position)
            text_field = QLineEdit(self)
            text_field.move(200, self.y_position)
            self.text_fields.append(text_field)
            self.y_position += 40

    def Button(self):
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.move(100, self.y_position + 20)
        self.clear_button = QPushButton('Clear', self)
        self.clear_button.move(200, self.y_position + 20)