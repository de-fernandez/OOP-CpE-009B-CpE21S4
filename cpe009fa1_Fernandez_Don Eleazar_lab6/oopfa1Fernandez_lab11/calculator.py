import sys
import math
from PyQt5.QtWidgets import (
    QGridLayout, QLineEdit, QPushButton, QWidget, QApplication, QMessageBox
)

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        names = [
            '7', '8', '9', '/', 'sin',
            '4', '5', '6', '*', 'cos',
            '1', '2', '3', '-', 'e',
            '0', '.', '=', '+', 'clear']

        self.textLine = QLineEdit(self)
        grid.addWidget(self.textLine, 0, 0, 1, 5)

        positions = [(i, j) for i in range(1, 6) for j in range(1, 6)]
        for position, name in zip(positions, names):
            button = QPushButton(name)
            button.clicked.connect(self.Button)
            grid.addWidget(button, *position)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Calculator')
        self.show()

    def Button(self):
        sender = self.sender()
        b_text = sender.text()

        if b_text == 'clear':
            self.textLine.clear()
        elif b_text == '=':
            self.Result()
        else:
            c_text = self.textLine.text()
            self.textLine.setText(c_text + b_text)

    def Result(self):
        try:
            expression = self.textLine.text()
            if 'sin' in expression:
                angle = self.getAngle(expression, 'sin')
                if angle is not None:
                    result = math.sin(math.radians(angle))
                    self.textLine.setText(str(result))
                    return

            if 'cos' in expression:
                angle = self.getAngle(expression, 'cos')
                if angle is not None:
                    result = math.cos(math.radians(angle))
                    self.textLine.setText(str(result))
                    return

            expression = expression.replace('e', str(math.e))
            result = eval(expression)
            self.textLine.setText(str(result))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Invalid input: {e}")

    def getAngle(self, expression, function):
        try:
            start = expression.index(function) + len(function)
            Angle = ''
            while start < len(expression) and (expression[start].isdigit() or expression[start] == '.'):
                Angle += expression[start]
                start += 1
            
            if Angle:
                return float(Angle)
            else:
                return None
        except ValueError:
            return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    sys.exit(app.exec_())