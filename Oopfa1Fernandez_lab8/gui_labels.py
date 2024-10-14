import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QToolTip, QLabel
from PyQt5.QtGui import QIcon

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt Line Edit'
        self.x = 200
        self.y = 200
        self.width = 300
        self.height = 300
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setWindowIcon(QIcon('pythonico.ico'))
        
        self.textbox1b1 = QLabel("Hello World!", self)
        self.textbox1b1.move(30, 25)
        self.textbox1b2 = QLabel("This program is written in Pycharm!", self)
        self.textbox1b2.move(30, 40)
        
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
