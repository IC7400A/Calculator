# ui/main_window.py
# Defines the main application window with a modern "frosted glass" effect.

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGraphicsBlurEffect
from PySide6.QtCore import Qt
from ui.theme import get_stylesheet, LIGHT_THEME, DARK_THEME

class CalculatorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setMinimumSize(400, 600)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.background = QWidget(self)
        self.background.setObjectName("background")
        
        blur_effect = QGraphicsBlurEffect(self)
        blur_effect.setBlurRadius(35)
        self.background.setGraphicsEffect(blur_effect)

        self.current_theme = DARK_THEME
        self.setStyleSheet(get_stylesheet(self.current_theme))
        
        self.init_ui()

    def resizeEvent(self, event):
        self.background.setGeometry(self.rect())
        super().resizeEvent(event)

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(5)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        top_bar = QHBoxLayout()
        self.shift_indicator = QLabel("")
        self.shift_indicator.setObjectName("indicator")
        self.deg_rad_indicator = QLabel("DEG")
        self.deg_rad_indicator.setObjectName("indicator")
        
        self.theme_toggle = QPushButton("☀️")
        self.theme_toggle.setObjectName("themeToggle")
        self.theme_toggle.setCheckable(True)
        self.theme_toggle.setChecked(True)
        self.theme_toggle.clicked.connect(self.toggle_theme)

        top_bar.addWidget(self.shift_indicator)
        top_bar.addStretch()
        top_bar.addWidget(self.deg_rad_indicator)
        top_bar.addWidget(self.theme_toggle)
        
        self.expression_label = QLabel("")
        self.expression_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.expression_label.setObjectName("expressionLabel")
        
        self.display = QLabel("0")
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setObjectName("mainDisplay")

        self.main_layout.addLayout(top_bar)
        self.main_layout.addWidget(self.expression_label)
        self.main_layout.addWidget(self.display)

    def toggle_theme(self):
        is_dark = self.theme_toggle.isChecked()
        self.current_theme = DARK_THEME if is_dark else LIGHT_THEME
        self.theme_toggle.setText("☀️" if is_dark else "🌙")
        self.setStyleSheet(get_stylesheet(self.current_theme))