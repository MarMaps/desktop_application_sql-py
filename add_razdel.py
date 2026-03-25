from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                           QPushButton, QMessageBox)
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtCore import Qt

class AddRazdel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить новый раздел')
        self.setGeometry(400, 300, 500, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel('Название раздела:'))
        self.nameRazd_input = QLineEdit()
        layout.addWidget(self.nameRazd_input)

        layout.addStretch()

        buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton('Сохранить')
        self.save_btn.clicked.connect(self.save_data)
        buttons_layout.addWidget(self.save_btn)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def save_data(self):
        name = self.nameRazd_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, 'Ошибка', 'Введите название раздела!')
            return

        query = QSqlQuery()
        query.prepare("INSERT INTO razdely (razdel) VALUES (:name)")
        query.bindValue(":name", name)
        
        if query.exec_():
            QMessageBox.information(self, 'Успех', 'Раздел успешно добавлен!')
            self.nameRazd_input.clear()