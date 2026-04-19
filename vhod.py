from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
import sys


class VhodWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle('Вход')
        self.setGeometry(400, 300, 300, 150)

        self.login_label = QLabel('Логин:')
        self.login_input = QLineEdit()

        self.parol_label = QLabel('Пароль:')
        self.parol_input = QLineEdit()
        self.parol_input.setEchoMode(QLineEdit.Password)

        self.vhod_button = QPushButton('Войти')
        self.vhod_button.clicked.connect(self.login_user)

        layout = QVBoxLayout()
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_input)
        layout.addWidget(self.parol_label)
        layout.addWidget(self.parol_input)
        layout.addWidget(self.vhod_button)

        self.setLayout(layout)

    def login_user(self):
        import main_user
        import main_admin

        login = self.login_input.text().strip()
        parol = self.parol_input.text().strip()

        if login == '' or parol == '':
            QMessageBox.warning(self, 'Ошибка', 'Заполните все поля!')
            return

        query = QSqlQuery()
        sql = """select id, login, parol, yr_dopuska from polzovateli
            where login = :login"""

        query.prepare(sql)
        query.bindValue(':login', login)
        
        if not query.exec_():
            QMessageBox.critical(self, 'Ошибка', f'Ошибка запроса: {query.lastError().text()}')
            return

        if query.next():
            id_polz = query.value(0)
            db_parol = query.value(2)
            yr_dopuska = query.value(3)

            if db_parol == parol:
                if yr_dopuska == 'user':
                    QMessageBox.information(self, 'Успех', 'Добро пожаловать!')
                    self.close()
                    if self.main_window:
                        self.main_window.update_role(id_polz, 'user')
                    else:
                        self.user_window = main_user.Window(id_polz)
                        self.user_window.show()
                elif yr_dopuska == 'admin':
                    QMessageBox.information(self, 'Администратор', 'Добро пожаловать!')
                    self.close()
                    if self.main_window:
                        self.main_window.update_role(id_polz, 'admin')
                    else:
                        self.admin_window = main_admin.Window()
                        self.admin_window.show()
                else:
                    QMessageBox.warning(self, 'Ошибка', f'У вас нет доступа. Уровень допуска: {yr_dopuska}')
            else:
                QMessageBox.critical(self, 'Ошибка', 'Неверный логин или пароль!')
        else:
            QMessageBox.critical(self, 'Ошибка', 'Пользователь не найден!')
