import sys
import os
import platform
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton,
    QLineEdit, QSizePolicy
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from interface import lib


def resource_path(relative_path):
    """ Get absolute path to resource, works for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(360, 500)

        icon_path = resource_path("./icon.ico")  # icon.png should be in the same directory
        self.setWindowIcon(QIcon(icon_path))


        self.setStyleSheet(self.styles())
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Small expression label
        self.expression_label = QLineEdit()
        self.expression_label.setReadOnly(True)
        self.expression_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.expression_label.setFixedHeight(30)
        self.expression_label.setStyleSheet("font-size: 16px; color: #666; background: #f3f3f3; border: none;")
        main_layout.addWidget(self.expression_label)

        # Main result display
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFixedHeight(70)
        self.display.setStyleSheet("font-size: 28px; color: black; background: white; padding: 10px; border-radius: 8px;")
        main_layout.addWidget(self.display)

        # Buttons grid
        grid = QGridLayout()
        buttons = [
            ('C', 0, 0), ('⌫', 0, 1), ('%', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('+/-', 4, 0), ('0', 4, 1), ('.', 4, 2), ('=', 4, 3),
        ]

        for text, row, col in buttons:
            btn = QPushButton(text)
            if text in ['+', '-', '*', '/', '%']:
                btn.setObjectName("operator")
            elif text == '=':
                btn.setObjectName("equals")
            else:
                btn.setObjectName("calcButton")

            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.clicked.connect(lambda _, t=text: self.handle_input(t))
            grid.addWidget(btn, row, col)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

        self.operand1 = ''
        self.operator = ''
        self.operand2 = ''

    def handle_input(self, text):
        if text in '0123456789.':
            if not self.operator:
                self.operand1 += text
                self.display.setText(self.operand1)
            else:
                self.operand2 += text
                self.display.setText(self.operand2)
                self.expression_label.setText(f"{self.operand1} {self.operator}")
        elif text in '+-*/':
            if self.operand1:
                self.operator = text
                self.expression_label.setText(f"{self.operand1} {self.operator}")
        elif text == '=':
            self.evaluate()
        elif text == 'C':
            self.clear()
        elif text == '⌫':
            self.backspace()
        elif text == '+/-':
            self.toggle_sign()
        elif text == '%':
            self.percent()

    def evaluate(self):
        try:
            a = float(self.operand1)
            b = float(self.operand2)
            result = None

            if self.operator == '+':
                result = lib.add(a, b)
            elif self.operator == '-':
                result = lib.sub(a, b)
            elif self.operator == '*':
                result = lib.mul(a, b)
            elif self.operator == '/':
                result = lib.divide(a, b) if b != 0 else "Err"

            self.expression_label.setText(f"{self.operand1} {self.operator} {self.operand2}")
            self.display.setText(str(result))
            self.operand1 = str(result)
            self.operand2 = ''
            self.operator = ''
        except Exception:
            self.display.setText('Error')
            self.clear()

    def toggle_sign(self):
        if self.operator and self.operand2:
            self.operand2 = str(-float(self.operand2))
            self.display.setText(self.operand2)
        elif self.operand1:
            self.operand1 = str(-float(self.operand1))
            self.display.setText(self.operand1)

    def percent(self):
        try:
            if self.operator and self.operand2:
                self.operand2 = str(float(self.operand2) / 100)
                self.display.setText(self.operand2)
            elif self.operand1:
                self.operand1 = str(float(self.operand1) / 100)
                self.display.setText(self.operand1)
        except:
            self.display.setText('Error')

    def backspace(self):
        if self.operator and self.operand2:
            self.operand2 = self.operand2[:-1]
            self.display.setText(self.operand2)
        elif not self.operator and self.operand1:
            self.operand1 = self.operand1[:-1]
            self.display.setText(self.operand1)

    def clear(self):
        self.operand1 = ''
        self.operand2 = ''
        self.operator = ''
        self.display.setText('')
        self.expression_label.setText('')

    def styles(self):
        return """
        QWidget {
            background-color: #f3f3f3;
        }
        QLineEdit {
            background-color: white;
        }
        QPushButton#calcButton {
            font-size: 20px;
            background-color: #eaeaea;
            color: #000;
            padding: 20px;
            border: none;
            border-radius: 12px;
        }
        QPushButton#calcButton:hover {
            background-color: #dcdcdc;
        }
        QPushButton#calcButton:pressed {
            background-color: #c0c0c0;
        }
        QPushButton#operator {
            font-size: 20px;
            background-color: #cfe8fc;
            color: black;
            padding: 20px;
            border: none;
            border-radius: 12px;
        }
        QPushButton#operator:hover {
            background-color: #b4ddf7;
        }
        QPushButton#equals {
            font-size: 20px;
            background-color: #0078d7;
            color: white;
            padding: 20px;
            border: none;
            border-radius: 12px;
        }
        QPushButton#equals:hover {
            background-color: #005fa3;
        }
        QPushButton#equals:pressed {
            background-color: #004e8c;
        }
        """


if __name__ == '__main__':
    app = QApplication([])
    win = Calculator()
    win.show()
    app.exec()