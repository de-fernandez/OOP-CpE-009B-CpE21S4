import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton

class Interface(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Special Midterm Exam in OOP"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.x = 200
        self.y = 200
        self.width = 420
        self.height = 320
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.button = QPushButton("Click to Change Color", self)
        self.button.move(158, 140)
        self.button.clicked.connect(self.color)
        self.show()
        
    def color(self):
        self.button.setStyleSheet('background-color: yellow')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Interface()
    sys.exit(app.exec_())