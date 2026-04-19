import os
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication


THEME_STYLES = {
    'light': """
        QMainWindow, QWidget {
            background-color: #f0f0f0;
        }
        QPushButton {
            background-color: #0078d7;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
        QTableWidget {
            background-color: white;
            gridline-color: #ccc;
        }
        QHeaderView::section {
            background-color: #e0e0e0;
            padding: 4px;
            border: 1px solid #ccc;
        }
        QLabel, QLineEdit {
            color: #333;
        }
    """,
    'dark': """
        QMainWindow, QWidget {
            background-color: #2b2b2b;
        }
        QPushButton {
            background-color: #0d89c4;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #1496d6;
        }
        QTableWidget {
            background-color: #3c3c3c;
            gridline-color: #555;
            color: #eee;
        }
        QHeaderView::section {
            background-color: #444;
            padding: 4px;
            border: 1px solid #555;
            color: #eee;
        }
        QLabel, QLineEdit {
            color: #eee;
        }
    """
}


class ThemeManager:
    def __init__(self, config_manager):
        self.config = config_manager
    
    def get_current_theme(self):
        return self.config.get_theme()
    
    def set_theme(self, theme):
        if theme in THEME_STYLES:
            self.config.set_theme(theme)
            self.apply_theme(theme)
    
    def apply_theme(self, theme=None):
        if theme is None:
            theme = self.get_current_theme()
        
        stylesheet = THEME_STYLES.get(theme, THEME_STYLES['light'])
        app = QApplication.instance()
        if app:
            app.setStyleSheet(stylesheet)
    
    def toggle_theme(self):
        current = self.get_current_theme()
        new_theme = 'dark' if current == 'light' else 'light'
        self.set_theme(new_theme)
        return new_theme