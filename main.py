# main.py
# The main entry point for the Calculator application.

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from core.calculator import Calculator

if __name__ == '__main__':
    # Ensure the application scales correctly on high-DPI displays.
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    
    window = Calculator()
    window.show()
    
    sys.exit(app.exec())