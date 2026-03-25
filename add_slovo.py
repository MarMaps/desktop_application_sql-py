from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                           QPushButton, QMessageBox)
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtCore import Qt

class AddSlovo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить ключевое слово')
        self.setGeometry(400, 300, 500, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel('Ключевое слово:'))
        self.slovo_input = QLineEdit()
        layout.addWidget(self.slovo_input)

        layout.addStretch()

        buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton('Сохранить')
        self.save_btn.clicked.connect(self.save_data)
        buttons_layout.addWidget(self.save_btn)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def save_data(self):
        slovo = self.slovo_input.text().strip()

        if not slovo:
            QMessageBox.warning(self, 'Ошибка', 'Введите ключевое слово!')
            return

        query = QSqlQuery()
        query.prepare("INSERT INTO cluch_slova (slovo) VALUES (:slovo)")
        query.bindValue(":slovo", slovo)

        if query.exec_():
            QMessageBox.information(self, 'Успех', 'Ключевое слово успешно добавлено!')
            self.slovo_input.clear()
