import sys
import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout, QCheckBox)
from PyQt5.QtSql import QSqlDatabase
from config_manager import ConfigManager, get_user_config_dir

class DatabaseConfigWindow(QDialog):
    def __init__(self, username=None):
        super().__init__()
        self.setWindowTitle("Настройка подключения к базе данных")
        self.resize(350, 320)
        self.db_info = {}
        self.username = username or "default"
        self.config = ConfigManager(self.username)

        saved_db = self.config.get_db_connection()
        
        # 1. Создаём поля ввода
        if saved_db:
            self.host_edit = QLineEdit(saved_db.get('host', 'localhost'))
            self.db_name_edit = QLineEdit(saved_db.get('db_name', 'ssylki'))
            self.port_edit = QLineEdit(str(saved_db.get('port', 5432)))
            self.user_edit = QLineEdit(saved_db.get('user', 'postgres'))
            self.pass_edit = QLineEdit(saved_db.get('password', '123456'))
        else:
            self.host_edit = QLineEdit("localhost")
            self.db_name_edit = QLineEdit("ssylki")
            self.port_edit = QLineEdit("5432")
            self.user_edit = QLineEdit("postgres")
            self.pass_edit = QLineEdit("123456")
        
        self.pass_edit.setEchoMode(QLineEdit.Password)
        
        self.save_checkbox = QCheckBox("Сохранить настройки подключения")
        self.save_checkbox.setChecked(bool(saved_db))

        # 2. Собираем форму с подписями
        form_layout = QFormLayout()
        form_layout.addRow("Хост:", self.host_edit)
        form_layout.addRow("Имя базы данных:", self.db_name_edit)
        form_layout.addRow("Порт:", self.port_edit)
        form_layout.addRow("Пользователь:", self.user_edit)
        form_layout.addRow("Пароль:", self.pass_edit)
        form_layout.addRow("", self.save_checkbox)

        # 3. Кнопки
        btn_layout = QHBoxLayout()
        self.connect_btn = QPushButton("Подключиться")
        self.connect_btn.clicked.connect(self.try_connect)
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)  # Закрывает окно с кодом "Отмена"

        btn_layout.addWidget(self.connect_btn)
        btn_layout.addWidget(self.cancel_btn)

        # 4. Главный лейаут
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def try_connect(self):
        # Считываем данные из полей
        host = self.host_edit.text().strip()
        db_name = self.db_name_edit.text().strip()
        port_str = self.port_edit.text().strip()
        user = self.user_edit.text().strip()
        password = self.pass_edit.text()

        # Простая валидация
        if not all([host, db_name, port_str, user]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        try:
            port = int(port_str)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Порт должен быть числом!")
            return

        # Сохраняем настройки если выбран чекбокс
        if self.save_checkbox.isChecked():
            self.config.set_db_connection(host, db_name, port, user, password)
        elif os.path.exists(self.config.config_file):
            os.remove(self.config.config_file)

        temp_db = QSqlDatabase.addDatabase("QPSQL", "temp_validation")
        temp_db.setHostName(host)
        temp_db.setDatabaseName("postgres")
        temp_db.setPort(port)
        temp_db.setUserName(user)
        temp_db.setPassword(password)

        if temp_db.open():
            self.db_info = {
                'host': host,
                'db_name': db_name,
                'port': port,
                'user': user,
                'password': password
            }
            temp_db.close()
            QSqlDatabase.removeDatabase("temp_validation")
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка подключения", 
                               f"Неверные данные сервера:\n{temp_db.lastError().text()}")
            temp_db.close()
            QSqlDatabase.removeDatabase("temp_validation")

        # Настраиваем подключение
        # db = QSqlDatabase.addDatabase("QPSQL")  # Создаёт подключение по умолчанию
        # db.setHostName(host)
        # db.setDatabaseName(db_name)
        # db.setPort(port)
        # db.setUserName(user)
        # db.setPassword(password)

        # # Пробуем открыть
        # if db.open():
        #     # QMessageBox.information(self, "Успех", "Подключение к базе данных успешно установлено!")
        #     self.accept()  # Закрывает окно с кодом "Успешно"
        # else:
        #     QMessageBox.critical(self, "Ошибка подключения", 
        #                          f"Не удалось подключиться:\n{db.lastError().text()}")
        #     db.close()  # Обязательно закрываем при ошибке, чтобы можно было попробовать снова