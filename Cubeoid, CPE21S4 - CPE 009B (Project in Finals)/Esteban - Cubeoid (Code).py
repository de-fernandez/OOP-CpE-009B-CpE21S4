import sys
import math
import cmath
import re
import numpy as np
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QPushButton, QWidget, QApplication, QMessageBox, QStackedWidget, QComboBox, QTextEdit
from PyQt5.QtCore import Qt
from sympy import symbols, diff, sympify, integrate
from fractions import Fraction

class ScientificCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.history = []
        self.initUI()
        self.memory = None

    def initUI(self):
        mainLayout = QGridLayout(self)
        mainLayout.setContentsMargins(20, 20, 20, 20)

        # The Page
        self.StackedWidget = QStackedWidget(self)
        self.MainPage = QWidget()
        self.ComplexPage = QWidget()
        self.BaseNPage = QWidget()
        self.PhysicsPage = QWidget()
        self.ShapesPage = QWidget()
        self.HistoryPage = QWidget()

        self.MainGrid = QGridLayout()
        self.ComplexGrid = QGridLayout()
        self.BaseNGrid = QGridLayout()
        self.PhysicsGrid = QGridLayout()
        self.ShapesGrid = QGridLayout()
        self.HistoryGrid = QGridLayout()

        self.Button(self.MainGrid)
        self.MainPage.setLayout(self.MainGrid)

        self.ComplexButtons(self.ComplexGrid)
        self.ComplexPage.setLayout(self.ComplexGrid)

        self.BaseNButtons(self.BaseNGrid)
        self.BaseNPage.setLayout(self.BaseNGrid)
        
        self.PhysicsButton(self.PhysicsGrid)
        self.PhysicsPage.setLayout(self.PhysicsGrid)
        
        self.ShapesButton(self.ShapesGrid)
        self.ShapesPage.setLayout(self.ShapesGrid)
        
        self.HistoryPanel = QTextEdit(self)
        self.HistoryPanel.setReadOnly(True)
        self.HistoryPanel.setStyleSheet("font-size: 16px;")
        self.HistoryGrid.addWidget(self.HistoryPanel)
        self.HistoryPage.setLayout(self.HistoryGrid)

        self.StackedWidget.addWidget(self.MainPage)
        self.StackedWidget.addWidget(self.ComplexPage)
        self.StackedWidget.addWidget(self.BaseNPage)
        self.StackedWidget.addWidget(self.PhysicsPage)
        self.StackedWidget.addWidget(self.ShapesPage)
        self.StackedWidget.addWidget(self.HistoryPage)

        # The Combobox
        self.ComboBox = QComboBox(self)
        self.ComboBox.addItem("Menu")
        self.ComboBox.addItem("Complex")
        self.ComboBox.addItem("Base - N")
        self.ComboBox.addItem("Physics")
        self.ComboBox.addItem("Shapes")
        self.ComboBox.addItem("History")
        self.ComboBox.currentIndexChanged.connect(self.ChangePage)
        self.ComboBox.setFixedSize(160, 40)
        self.ComboBox.setStyleSheet("QComboBox {font-size: 16px; border-radius: 20px; padding-left: 18px;} QComboBox::drop-down {border: 0px;width: 0px;}")

        self.textLine = QLineEdit(self)
        self.textLine.setFixedHeight(80)
        self.textLine.setStyleSheet("font-size: 24px;")
        self.textLine.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        mainLayout.addWidget(self.textLine, 0, 0, 1, 5)
        mainLayout.addWidget(self.ComboBox, 1, 2)
        mainLayout.addWidget(self.StackedWidget, 2, 0, 1, 5)
        

        self.setGeometry(1400, 200, 400, 700)
        self.setWindowTitle('Cubeoid - V1')
        self.setLayout(mainLayout)
        self.show()

    def Button(self, grid):
        functions = [
            ('²√', 2, 0), ('³√', 2, 1), ('𝑥ⁿ', 2, 2), ('𝑥²', 2, 3), ('X', 2, 4),
            ('(-)', 3, 0), ('(', 3, 1), (')', 3, 2), ('π', 3, 3), ('𝑒', 3, 4),
            ('ln', 4, 0), ('log₁₀', 4, 1), ('sin', 4, 2), ('cos', 4, 3), ('tan', 4, 4),
            ('!', 5, 0), ('nPr', 5, 1), ('nCr', 5, 2), ('d/dx', 5, 3), ('∫', 5, 4),
            ('*', 6, 0), ('/', 6, 1), ('%', 6, 2), ('S ↔ D', 6, 4)
        ]
        
        keypad = [
            '7', '8', '9', 'Del', 'AC',
            '4', '5', '6', '×', '÷',
            '1', '2', '3', '+', '-',
            '0', '.', 'x10ⁿ', '='
        ]

        for name, row, col in functions:
            button = QPushButton(name)
            button.setFixedSize(60, 40)
            button.setStyleSheet("font-size: 16px;")
            button.clicked.connect(self.Function)
            grid.addWidget(button, row, col)

        keypadPositions = [(i, j) for i in range(7, 11) for j in range(5)]
        for position, name in zip(keypadPositions, keypad):
            button = QPushButton(name)
            button.setFixedSize(60, 40)
            button.setStyleSheet("font-size: 16px;")
            button.clicked.connect(self.Function)
            grid.addWidget(button, *position)
            
    def ComplexButtons(self, grid):
        functions = [
            ('²√', 2, 0, ''), ('³√', 2, 1, ''), ('𝑥ⁿ', 2, 2, ''), ('𝑥²', 2, 3, ''), ('*', 2, 4, ''),
            ('(-)', 3, 0, ''), ('(', 3, 1, ''), (')', 3, 2, ''), ('π', 3, 3, ''), ('𝑒', 3, 4, ''),
            ('ln', 4, 0, ''), ('log₁₀', 4, 1, ''), ('sin', 4, 2, ''), ('cos', 4, 3, ''), ('tan', 4, 4, ''),
            ('Arg', 5, 0, 'Input: Arg(a + bi)'), ('Conjg', 5, 1, 'Input: Conjg(a + bi)'), ('∠', 5, 2, 'Input: R∠θ'), ('i', 5, 3, 'Input: a + bi')
        ]
        
        keypad = [
            '7', '8', '9', 'Del', 'AC',
            '4', '5', '6', '×', '÷',
            '1', '2', '3', '+', '-',
            '0', '.', '×10ⁿ', '='
        ]
        
        for name, row, col, tooltip in functions:
            button = QPushButton(name)
            button.setFixedSize(60, 40)
            button.setStyleSheet("font-size: 16px;")
            button.setToolTip(tooltip)
            button.clicked.connect(self.Function)
            grid.addWidget(button, row, col)

        keypadPositions = [(i, j) for i in range(7, 11) for j in range(5)]
        for position, name in zip(keypadPositions, keypad):
            button = QPushButton(name)
            button.setFixedSize(60, 40)
            button.setStyleSheet("font-size: 16px;")
            button.clicked.connect(self.Function)
            grid.addWidget(button, *position)
            
    def BaseNButtons(self, grid):
        functions = [
            ('²√', 2, 0), ('³√', 2, 1), ('𝑥ⁿ', 2, 2), ('𝑥²', 2, 3), ('*', 2, 4),
            ('(-)', 3, 0), ('(', 3, 1), (')', 3, 2), ('π', 3, 3), ('𝑒', 3, 4),
            ('ln', 4, 0), ('log₁₀', 4, 1), ('sin', 4, 2), ('cos', 4, 3), ('tan', 4, 4),
            ("BIN", 5, 0), ("OCT", 5, 1), ("DEC", 5, 2), ("HEX", 5, 3)
        ]
        
        keypad = [
            '7', '8', '9', 'Del', 'AC',
            '4', '5', '6', '×', '÷',
            '1', '2', '3', '+', '-',
            '0', '.', '×10ⁿ', '='
        ]

        for name, row, col in functions:
            button = QPushButton(name)
            button.setFixedSize(60, 40)
            button.setStyleSheet("font-size: 16px;")
            button.clicked.connect(self.Function)
            grid.addWidget(button, row, col)

        keypadPositions = [(i, j) for i in range(7, 11) for j in range(5)]
        for position, name in zip(keypadPositions, keypad):
            button = QPushButton(name)
            button.setFixedSize(60, 40)
            button.setStyleSheet("font-size: 16px;")
            button.clicked.connect(self.Function)
            grid.addWidget(button, *position)
            
    def PhysicsButton(self, grid):
        functions = [
            ('²√', 2, 0, ''), ('³√', 2, 1, ''), ('𝑥ⁿ', 2, 2, ''), ('𝑥²', 2, 3, ''), ('*', 2, 4, ''),
            ('(-)', 3, 0, ''), ('(', 3, 1, ''), (')', 3, 2, ''), ('π', 3, 3, ''), ('𝑒', 3, 4, ''),
            ('ln', 4, 0, ''), ('log₁₀', 4, 1, ''), ('sin', 4, 2, ''), ('cos', 4, 3, ''), ('tan', 4, 4, ''),
            ('𝑣', 5, 0, 'Final Velocity Input: v,a,t,𝑣'), ('Δ𝑑', 5, 1, 'Displacement Input: v,a,t,Δ𝑑'), ('𝐹', 5, 2, 'Force Input: m,a,𝐹'), ('𝑃', 5, 3, 'Power Input: W,t,𝑃'), ('𝑝', 5, 4, 'Momentum Input: m,v,𝑝'),
            ('Δ𝑈', 6, 0, 'Change in Internal Energy Input: Q,W,Δ𝑈'), ('𝑇(IGL)', 6, 1, 'Temperature in Ideal Gas Law Input: P,V,n,𝑇(IGL)'), (',', 6, 2, '')
        ]
        
        keypad = [
            '7', '8', '9', 'Del', 'AC',
            '4', '5', '6', '×', '÷',
            '1', '2', '3', '+', '-',
            '0', '.', '×10ⁿ', '='
        ]

        for name, row, col, tooltip in functions:
            button = QPushButton(name)
            button.setFixedSize(60, 40)
            button.setStyleSheet("font-size: 16px;")
            button.setToolTip(tooltip)
            button.clicked.connect(self.Function)
            grid.addWidget(button, row, col)

        keypadPositions = [(i, j) for i in range(7, 11) for j in range(5)]
        for position, name in zip(keypadPositions, keypad):
            button = QPushButton(name)
            button.setFixedSize(60, 40)
            button.setStyleSheet("font-size: 16px;")
            button.clicked.connect(self.Function)
            grid.addWidget(button, *position)
            
    def ShapesButton(self, grid):
        functions = [
            ('²√', 2, 0, ''), ('³√', 2, 1, ''), ('𝑥ⁿ', 2, 2, ''), ('𝑥²', 2, 3, ''), ('*', 2, 4, ''),
            ('(-)', 3, 0, ''), ('(', 3, 1, ''), (')', 3, 2, ''), ('π', 3, 3, ''), ('𝑒', 3, 4, ''),
            ('ln', 4, 0, ''), ('log₁₀', 4, 1, ''), ('sin', 4, 2, ''), ('cos', 4, 3, ''), ('tan', 4, 4, ''),
            ('◯', 5, 0, 'Circle Input: R◯(A or P)'), ('□', 5, 1, 'Square Input: S□(A or P)'), ('△', 5, 2, 'Triangle Input: B,H△(A or P)'), ('▭', 5, 3, 'Rectangle Input: L,W▭(A or P)'), (',', 5, 4, ''),
            ('A', 6, 0, 'Area'), ('P', 6, 1, 'Perimeter')
        ]
        
        keypad = [
            '7', '8', '9', 'Del', 'AC',
            '4', '5', '6', '×', '÷',
            '1', '2', '3', '+', '-',
            '0', '.', '×10ⁿ', '='
        ]

        for name, row, col, tooltip in functions:
            button = QPushButton(name)
            button.setFixedSize(60, 40)
            button.setStyleSheet("font-size: 16px;")
            button.setToolTip(tooltip)
            button.clicked.connect(self.Function)
            grid.addWidget(button, row, col)

        keypadPositions = [(i, j) for i in range(7, 11) for j in range(5)]
        for position, name in zip(keypadPositions, keypad):
            button = QPushButton(name)
            button.setFixedSize(60, 40)
            button.setStyleSheet("font-size: 16px;")
            button.clicked.connect(self.Function)
            grid.addWidget(button, *position)
            
    def Function(self):
        sender = self.sender()
        
        Button = sender.text()
        if Button == 'Del':
            self.Delete()
        elif Button == 'AC':
            self.textLine.clear()
        elif Button == '=':
            self.Result()
        elif Button == '(-)':
            self.negativeSign()
        elif Button == 'S ↔ D':
            expression = self.textLine.text().strip()
            if '/' in expression:
                numerator, denominator = map(int, expression.split('/'))
                if denominator == 0:
                    return "Math ERROR"
                result = numerator / denominator
                self.textLine.setText(f"{result:.2f}")
            else:
                decimal = float(expression)
                result = Fraction(decimal).limit_denominator()
                self.textLine.setText(str(result))
        else:
            inputText = self.textLine.text()
            self.textLine.setText(inputText + Button)
    
    def Delete(self):
        inputText = self.textLine.text()
        if inputText:
            deletedText = inputText[:-1]
            self.textLine.setText(deletedText)
    
    def negativeSign(self):
        inputText = self.textLine.text()
        if inputText:
            if inputText.startswith('-'):
                negativeText = inputText[1:]
            else:
                negativeText = '-' + inputText
            self.textLine.setText(negativeText)
    
    def Result(self):
        expression = self.textLine.text()
        
        # The Function
        if '%' in expression:
            expression = expression.split('%')
            if len(expression) == 2:
                base = eval(expression[0].strip())
                result = (1 / 100) * base
                self.textLine.setText(str(result))
        elif '²√' in expression or '³√' in expression:
            expression = expression.replace('²√', 'np.sqrt')
            expression = expression.replace('³√', 'np.cbrt')
        elif '𝑥ⁿ' in expression or '𝑥²' in expression:
            expression = expression.replace('𝑥ⁿ', '**')
            expression = expression.replace('𝑥²', '**2')
        elif 'ln' in expression or 'log₁₀' in expression:
            expression = expression.replace('ln', 'np.log')
            expression = expression.replace('log₁₀', 'np.log10')
        elif 'sin' in expression or 'cos' in expression or 'tan' in expression:
            expression = expression.replace('sin', 'np.sin(np.radians')
            expression = expression.replace('cos', 'np.cos(np.radians')
            expression = expression.replace('tan', 'np.tan(np.radians')
            expression = expression.replace(')', '))', 1)
        elif '!' in expression:
            parts = expression.split('!')
            expression = parts[0].strip()
            if expression:
                expression = int(expression)
                if expression < 0:
                    self.textLine.setText("Math ERROR: Factorial of negative number is undefined.")
                else:
                    result = math.factorial(expression)
                    self.textLine.setText(f"{result}")
        elif 'π' in expression or '𝑒' in expression:
            expression = expression.replace('π', str(math.pi))
            expression = expression.replace('𝑒', str(math.e))
        elif 'nPr' in expression:
            n, r = map(int, expression.split('nPr'))
            if n < 0 or r < 0 or n < r:
                self.textLine.setText("Math ERROR")
            else:
                result = math.factorial(n) // math.factorial(n - r)
                self.textLine.setText(f"{result}")
        elif 'nCr' in expression:
            n, r = map(int, expression.split('nCr'))
            if n < 0 or r < 0 or n < r:
                self.textLine.setText("Math ERROR")
            else:
                result = math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
                self.textLine.setText(f"{result}")
        elif 'd/dx' in expression:
            expression = expression.split('d/dx')[1].strip()
            x = symbols('X')
            try:
                func = sympify(expression)
                derivative = diff(func, x)
                self.textLine.setText(f"{derivative}")
                return
            except:
                self.textLine.setText("Math ERROR")
                return
        elif '∫' in expression:
            if '∫' in expression:
                expression = expression.split('∫')[1].strip()
                x = symbols('X')
                expression = sympify(expression)
                result = integrate(expression, x)
                self.textLine.setText(f"{result} + C")
                return
            expression = expression.replace('×', '*').replace('÷', '/')
            result = eval(expression)
            self.textLine.setText(str(result))
        elif '×' in expression or '÷' in expression:
            expression = expression.replace('×', '*').replace('÷', '/')
        elif 'x10ⁿ' in expression:
            expression = re.sub(r'(\d+|\d+\.\d+)\s*x\s*10\ⁿ(\d+)', r'\1 * (10**\2)', expression)
        elif 'BIN' in expression:
            num = int(expression.split("BIN")[1].strip())
            result = bin(num)[2:]
            self.textLine.setText(f"{result}")
        elif 'OCT' in expression:
            num = int(expression.split("OCT")[1].strip())
            result = oct(num)[2:]
            self.textLine.setText(f"{result}")
        elif 'DEC' in expression:
            num = int(expression.split("DEC")[1].strip())
            result = str(num)
            self.textLine.setText(f"{result}")
        elif 'HEX' in expression:
            num = int(expression.split("HEX")[1].strip())
            result = hex(num)[2:].upper()
            self.textLine.setText(f"{result}")
        elif "Arg" in expression:
            expression = re.match(r'Arg\(([-+]?\d*\.?\d+)([-+]\d*\.?\d+)i\)', expression)
            a = float(expression[1])
            b = float(expression[2])
            rad = math.atan2(b, a)
            theta = math.degrees(rad)
            self.textLine.setText(f"{theta:.2f}°")
        elif "Conjg" in expression:
            expression = re.match(r'Conjg\(\s*([-+]?\d*\.?\d+)\s*([-+])\s*(\d*\.?\d+)i\s*\)', expression)
            a = float(expression[1])
            sign = expression[2]
            b = float(expression[3])
            if sign == '+':
                conjugate = f"{a} - {b}i"
            else:
                conjugate = f"{a} + {b}i"
            self.textLine.setText(f"{conjugate}")
        elif '∠' in expression:
            angle = expression.split('∠')
            r = float(angle[0].strip())
            result = float(angle[1].strip())
            result = r * (math.cos(math.radians(result)) + 1j * math.sin(math.radians(result)))
            self.textLine.setText(f"{result:.4f}")
        elif 'i' in expression:
            expression = expression.replace(' ', '').replace('i', '')
            if '+' in expression:
                expression = expression.split('+')
            elif '-' in expression[1:]:
                expression = expression.split('-', 1)
                expression[1] = '-' + expression[1]
            a = float(expression[0])
            b = float(expression[1])
            r = math.sqrt(a**2 + b**2)
            theta = math.degrees(math.atan2(b, a))
            result = f"{r:.2f}∠{theta:.2f}"
            self.textLine.setText(f"{result}")
        elif '𝑣' in expression:
            u = float(self.textLine.text().split(',')[0])
            a = float(self.textLine.text().split(',')[1])
            t = float(self.textLine.text().split(',')[2])
            v = u + a * t
            self.textLine.setText(f"{v:.2f} m/s")
        elif 'Δ𝑑' in expression:
            u = float(self.textLine.text().split(',')[0])
            a = float(self.textLine.text().split(',')[1])
            t = float(self.textLine.text().split(',')[2])
            s = u * t + 0.5 * a * t ** 2
            self.textLine.setText(f"{s:.2f} m")
        elif '𝐹' in expression:
            m = float(self.textLine.text().split(',')[0])
            a = float(self.textLine.text().split(',')[1])
            F = m * a
            self.textLine.setText(f"{F:.2f} N")
        elif '𝑃' in expression:
            W = float(self.textLine.text().split(',')[0])
            t = float(self.textLine.text().split(',')[1])
            P = W / t
            self.textLine.setText(f"{P:.2f} W")
        elif '𝑝' in expression:
            m = float(self.textLine.text().split(',')[0])
            v = float(self.textLine.text().split(',')[1])
            p = m * v
            self.textLine.setText(f"{p:.2f} kg·m/s")
        elif 'Δ𝑈' in expression:
            Q = float(self.textLine.text().split(',')[0])
            W = float(self.textLine.text().split(',')[1])
            ΔU = Q - W
            self.textLine.setText(f"{ΔU:.2f} J")
        elif '𝑇(IGL)' in expression:
            P = float(self.textLine.text().split(',')[0])
            V = float(self.textLine.text().split(',')[1])
            n = float(self.textLine.text().split(',')[2])
            R = 8.314
            T = (P * V) / (n * R)
            self.textLine.setText(f"{T:.2f} K")             
        elif '◯' in expression:
            parts = expression.split('◯')
            radius = float(parts[0].strip())
            if 'A' in expression:
                area = math.pi * (radius ** 2)
                self.textLine.setText(f"{area:.2f}")
            elif 'P' in expression:
                circumference = 2 * math.pi * radius
                self.textLine.setText(f"{circumference:.2f}")
            return
        elif '□' in expression:
            parts = expression.split('□')
            side = float(parts[0].strip())
            if 'A' in expression:
                area = side ** 2
                self.textLine.setText(f"{area:.2f}")
            elif 'P' in expression:
                perimeter = 4 * side
                self.textLine.setText(f"{perimeter:.2f}")
        elif '▭' in expression:
            if ',' in expression:
                length, rest = expression.split(',')
                width, operation = rest.split('▭')
                length = float(length)
                width = float(width)
            else:
                parts = expression.split('▭')
                length = float(parts[0].strip())
                width = length
            if 'A' in expression:
                area = length * width
                self.textLine.setText(f"{area:.2f}")
            elif 'P' in expression:
                perimeter = 2 * (length + width)
                self.textLine.setText(f"{perimeter:.2f}")
        elif '△' in expression:
            if ',' in expression:
                parts = expression.split('△')
                base_height = parts[0].strip().split(',')
                if len(base_height) == 2:
                    base = float(base_height[0])
                    height = float(base_height[1])
                    if 'A' in expression:
                        area = 0.5 * base * height
                        self.textLine.setText(f"{area:.2f}")
                    elif 'P' in expression:
                        hypotenuse = math.sqrt(base**2 + height**2)
                        perimeter = base + height + hypotenuse
                        self.textLine.setText(f"{perimeter:.2f}")
        else:
            self.textLine.setText("Math ERROR")
            
        result = eval(expression)
        result = round(result, 2)
        self.textLine.setText(str(result))
        self.memory = result
        self.History(expression, result)
        
    def History(self, expression, result):
        expression = f"{expression} = {result}"
        self.history.append(expression)
        self.HistoryPanel.append(expression)
        
    def ChangePage(self):
        Index = self.ComboBox.currentIndex()
        self.StackedWidget.setCurrentIndex(Index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = ScientificCalculator()
    sys.exit(app.exec_())