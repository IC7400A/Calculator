# core/calculator.py
# The final logic engine, connecting the UI to the robust evaluator.

from PySide6.QtWidgets import QGridLayout, QPushButton
from PySide6.QtCore import Qt
from ui.main_window import CalculatorWindow
from core.evaluator import Evaluator
import math

class Calculator(CalculatorWindow):
    def __init__(self):
        super().__init__()
        self._create_button_grid()
        self.init_state()
        self._connect_signals()

    def init_state(self):
        self.is_shift = False
        self.is_hyp = False
        self.ans_value = "0"
        self.expression_label.setText("")
        self.display.setText("0")
        self.set_shift_mode(False)
        self.deg_rad_indicator.setText("DEG")

    def _create_button_grid(self):
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)
        
        self.buttons_map = {
            # (row, col): (text, shift_text)
            (0, 0): ("SHIFT", "SHIFT"), (0, 1): ("hyp", "hyp"),   (0, 2): ("x²", "x³"),      (0, 3): ("xʸ", "√"),     (0, 4): ("x⁻¹", "x⁻¹"),
            (1, 0): ("sin", "asin"),   (1, 1): ("cos", "acos"),   (1, 2): ("tan", "atan"),   (1, 3): ("DEL", "AC"),   (1, 4): ("Ans", "Ans"),
            (2, 0): ("log", "exp"),    (2, 1): ("ln", "!"),       (2, 2): ("(", "("),       (2, 3): (")", ")"),       (2, 4): ("%", "%"),
            (3, 0): ("7", "7"),       (3, 1): ("8", "8"),       (3, 2): ("9", "9"),       (3, 3): ("/", "/"),       (3, 4): ("x", "x"),
            (4, 0): ("4", "4"),       (4, 1): ("5", "5"),       (4, 2): ("6", "6"),       (4, 3): ("-", "-"),       (4, 4): ("+", "+"),
            (5, 0): ("1", "1"),       (5, 1): ("2", "2"),       (5, 2): ("3", "3"),       (5, 3): ("e", "e"),       (5, 4): ("π", "π"),
            (6, 0, 1, 2): ("0", "0"), (6, 2, 1, 1): (".", "."), (6, 3, 1, 2): ("=", "=")
        }

        for pos, (text, _) in self.buttons_map.items():
            button = QPushButton(text)
            grid_layout.addWidget(button, *pos)
        
        self.main_layout.addLayout(grid_layout)

    def _connect_signals(self):
        for button in self.findChildren(QPushButton):
            if button.objectName() != "themeToggle":
                button.clicked.connect(self._on_button_click)
        self.deg_rad_indicator.mousePressEvent = self.toggle_angle_mode

    def _on_button_click(self):
        button = self.sender()
        text = button.text()
        
        action_map = {
            "SHIFT": self.toggle_shift, "hyp": self.toggle_hyp,
            "AC": self.init_state, "DEL": self.backspace,
            "=": self.calculate, "Ans": lambda: self.append_to_expression(self.ans_value)
        }
        
        if text in action_map:
            action_map[text]()
        else:
            self.append_to_expression(text)
        
        if text not in ["SHIFT", "hyp"]:
            self.set_shift_mode(False)
            self.set_hyp_mode(False)

    def append_to_expression(self, text):
        if text == "xʸ": text = "^"
        
        if text in Evaluator().functions:
            text += "("
        self.expression_label.setText(self.expression_label.text() + text)

    def calculate(self):
        self.evaluator = Evaluator(self.deg_rad_indicator.text() == "RAD")
        expr = self.expression_label.text()
        if not expr: return
        try:
            result = self.evaluator.evaluate(expr)
            if math.isnan(result) or math.isinf(result):
                self.display.setText("Math Error")
            else:
                result_str = f"{result:.10g}"
                self.display.setText(result_str)
                self.ans_value = result_str
        except Exception as e:
            self.display.setText("Syntax Error")
            print(f"Evaluation Error: {e}")
    
    def toggle_shift(self):
        self.set_shift_mode(not self.is_shift)
        
    def toggle_hyp(self):
        self.set_hyp_mode(not self.is_hyp)

    def set_shift_mode(self, is_active):
        self.is_shift = is_active
        self.update_button_text()
        
    def set_hyp_mode(self, is_active):
        self.is_hyp = is_active
        self.update_button_text()
        
    def update_button_text(self):
        self.shift_indicator.setText(f"{'SHIFT' if self.is_shift else ''} {'HYP' if self.is_hyp else ''}".strip())
        grid = self.main_layout.itemAt(self.main_layout.count()-1)
        for pos, (text, shift_text) in self.buttons_map.items():
            button = grid.itemAtPosition(*pos[:2]).widget()
            if button:
                current_text = shift_text if self.is_shift else text
                if self.is_hyp and current_text in ["sin", "cos", "tan", "asin", "acos", "atan"]:
                    current_text = current_text.replace("sin", "sinh").replace("cos", "cosh").replace("tan", "tanh")
                button.setText(current_text)
            
    def toggle_angle_mode(self, event):
        self.deg_rad_indicator.setText("RAD" if self.deg_rad_indicator.text() == "DEG" else "DEG")

    def backspace(self):
        self.expression_label.setText(self.expression_label.text()[:-1])