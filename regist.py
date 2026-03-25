from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
import sys


class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Регистрация')
        self.setGeometry(400, 300, 300, 150)

        self.login_label = QLabel('Логин:')
        self.login_input = QLineEdit()

        self.parol_label = QLabel('Пароль:')
        self.parol_input = QLineEdit()
        self.parol_input.setEchoMode(QLineEdit.Password)

        self.reg_button = QPushButton('Зарегистрироваться')
        self.reg_button.clicked.connect(self.register_user)

        layout = QVBoxLayout()
        layout.addWidget(self.login_label)
        layout.addWidget(self.login_input)
        layout.addWidget(self.parol_label)
        layout.addWidget(self.parol_input)
        layout.addWidget(self.reg_button)

        self.setLayout(layout)

    def register_user(self):
        login = self.login_input.text().strip()
        parol = self.parol_input.text().strip()

        if login == '' or parol == '':
            QMessageBox.warning(self, 'Ошибка', 'Заполните все поля!')
            return

        query = QSqlQuery()
        sql = """insert into polzovateli (login, parol, yr_dopuska)
            values (:login, :parol, 'user')"""

        query.prepare(sql)
        query.bindValue(':login', login)
        query.bindValue(':parol', parol)

        if query.exec_():
            QMessageBox.information(self, 'Успех', 'Пользователь успешно зарегистрирован!')
            self.close()
        else:
            QMessageBox.critical(self, 'Ошибка', 'Ошибка при регистрации!\n' + query.lastError().text())


if __name__ == '__main__':
    if not QSqlDatabase.contains('qt_sql_default_connection'):
        db = QSqlDatabase.addDatabase('QPSQL')
        db.setHostName('localhost')
        db.setDatabaseName('ssylki')
        db.setPort(5432)
        db.setUserName('postgres')
        db.setPassword('123456')

        if not db.open():
            print('Ошибка подключения к базе данных')

    app = QApplication(sys.argv)
    window = RegistrationWindow()
    window.show()
    sys.exit(app.exec())
