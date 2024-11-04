import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSlot

class Interface(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Midterm in OOP"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(200, 200, 420, 200)
        
        self.label = QLabel("Enter your fullname:", self)
        self.label.move(40, 60)
        
        self.textbox = QLineEdit(self)
        self.textbox.move(200, 60)
        
        self.button = QPushButton("Click to display your Fullname", self)
        self.button.move(40, 95)
        self.button.clicked.connect(self.name)
        
        self.output_label = QLabel(self)
        self.output_label.move(200, 100)
    
    @pyqtSlot()
    def name(self):
        fullname = self.textbox.text()
        self.output_label.setText(fullname)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Interface()
    ex.show()
    sys.exit(app.exec_())