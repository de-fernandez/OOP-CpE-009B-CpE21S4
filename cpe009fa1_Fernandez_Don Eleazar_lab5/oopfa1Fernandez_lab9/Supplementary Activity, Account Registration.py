import sys
import csv
import os
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QLineEdit, QPushButton, QMessageBox

class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setWindowTitle('Account Registration')
        self.setGeometry(100, 100, 400, 400)
        self.fields = ['First Name', 'Last Name', 'Username', 'Password', 'Email Address', 'Contact Number']
        self.textbox = []

        for i, field in enumerate(self.fields):
            QLabel(field, self).move(50, 60 + i * 40)
            textbox = QLineEdit(self)
            textbox.move(200, 60 + i * 40)
            self.textbox.append(textbox)

        self.create_buttons()
    def create_buttons(self):
        QPushButton('Submit', self, clicked=self.register).move(100, 300)
        QPushButton('Clear', self, clicked=self.clear).move(200, 300)

    def clear(self):
        for textbox in self.textbox:
            textbox.clear()

    def register(self):
        data = [field.text() for field in self.textbox]
        if any(not value for value in data):
            QMessageBox.warning(self, "Missing Information", "Please fill out all fields.", QMessageBox.Ok)
            return

        file_exists = os.path.isfile('registrations.csv')
        with open('registrations.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(self.fields)
            writer.writerow(data)
        QMessageBox.information(self, "Registration Successful", "Account registered successfully!", QMessageBox.Ok)
        self.clear_fields()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegistrationWindow()
    sys.exit(app.exec_())