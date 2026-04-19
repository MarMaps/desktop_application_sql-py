# #!/usr/bin/python3
# import sys
# import io
# from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
#                              QLabel, QPushButton, QHBoxLayout)
# from PyQt5.QtSql import QSqlDatabase, QSqlQuery
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtCore import Qt
# from add_link import AddLinkWindow
# from search_window import SearchWindow
# from add_razdel import AddRazdel
# from add_slovo import AddSlovo
# from PyQt5.QtWidgets import QSizePolicy
# from regist import RegistrationWindow
# from vhod import VhodWindow


# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Ссылки')
#         self.setGeometry(300, 300, 1700, 1000)

#         self.table = QTableWidget()
#         self.table.setEditTriggers(QTableWidget.NoEditTriggers)
#         self.table.verticalHeader().hide()
#         self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

#         self.main_layout = QVBoxLayout()
#         self.main_layout.setAlignment(Qt.AlignTop)

#         top_panel_layout = QHBoxLayout()
#         #self.add_button = QPushButton('+ Добавить ссылку')
#         #self.add_razdel = QPushButton('+ Добавить раздел')
#         #self.add_slovo = QPushButton('+ Добавить ключевое слово')
#         self.search_button = QPushButton('Поиск')
#         #self.refresh_button = QPushButton('Обновить таблицу')
#         self.reg_button = QPushButton('Зарегистрироваться')
#         self.vhod_button = QPushButton('Вход')

#         #top_panel_layout.addWidget(self.add_button)
#         #top_panel_layout.addWidget(self.add_razdel)
#         #top_panel_layout.addWidget(self.add_slovo)
#         top_panel_layout.addWidget(self.search_button)
#         #top_panel_layout.addWidget(self.refresh_button)
#         top_panel_layout.addStretch()
#         top_panel_layout.addWidget(self.reg_button)
#         top_panel_layout.addWidget(self.vhod_button)
#         self.main_layout.addLayout(top_panel_layout)
#         self.main_layout.addWidget(self.table)
#         self.setLayout(self.main_layout)

#         #self.add_button.clicked.connect(self.open_add_window)
#         self.search_button.clicked.connect(self.open_search_window)
#         #self.add_razdel.clicked.connect(self.open_add_razdel)
#         #self.add_slovo.clicked.connect(self.open_add_slovo)
#         #self.refresh_button.clicked.connect(self.load_data)
#         self.reg_button.clicked.connect(self.open_registration_window)
#         self.vhod_button.clicked.connect(self.open_vhod_window)

#         self.load_data()
    
#     def open_add_window(self):
#         self.add_window = AddLinkWindow()
#         self.add_window.show()
#         self.add_window.destroyed.connect(self.load_data)

#     def open_search_window(self):
#         self.search_window = SearchWindow()
#         self.search_window.show()

#     def open_add_razdel(self):
#         self.add_razdel = AddRazdel()
#         self.add_razdel.show()
#         self.add_razdel.destroyed.connect(self.load_data)

#     def open_add_slovo(self):
#         self.add_slovo_window = AddSlovo()
#         self.add_slovo_window.show()
#         self.add_slovo_window.destroyed.connect(self.load_data)

#     def open_registration_window(self):
#         self.reg_window = RegistrationWindow()
#         self.reg_window.show()

#     def open_vhod_window(self):
#         self.vhod_window = VhodWindow()
#         self.vhod_window.show()

#     def load_data(self):
#         self.table.setRowCount(0)
#         q = QSqlQuery()
#         q.exec_('select naimen, ssylka, opisanie, skrinshot from ssylki_tab')

#         self.table.setColumnCount(4)
#         self.table.setHorizontalHeaderLabels(['Название', 'Ссылка', 'Описание', 'Снимок'])

#         row = 0
#         while q.next():
#             self.table.insertRow(row)

#             self.table.setItem(row, 0, QTableWidgetItem(str(q.value(0))))
#             self.table.setColumnWidth(0, 150)
#             self.table.setItem(row, 1, QTableWidgetItem(str(q.value(1))))
#             self.table.setColumnWidth(1, 180)
#             self.table.setItem(row, 2, QTableWidgetItem(str(q.value(2))))
#             self.table.setColumnWidth(2, 400)

#             img_data = q.value(3)
#             if img_data:
#                 pixmap = QPixmap()
#                 if pixmap.loadFromData(img_data):
#                     pixmap = pixmap.scaled(680, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation)
#                     label = QLabel()
#                     label.setPixmap(pixmap)
#                     label.setAlignment(Qt.AlignCenter)
#                     self.table.setRowHeight(row, 300)
#                     self.table.setColumnWidth(3, 700)
#                     self.table.setCellWidget(row, 3, label)
#                 else:
#                     self.table.setItem(row, 3, QTableWidgetItem('Ошибка конвертации'))
#             else:
#                 self.table.setItem(row, 3, QTableWidgetItem('Нет данных'))

#             row += 1


# # подключение к БД и запуск
# db = QSqlDatabase.addDatabase('QPSQL')
# db.setHostName('localhost')
# db.setDatabaseName('ssylki')
# db.setPort(5432)
# db.setUserName('postgres')
# db.setPassword('123456')

# if not db.open():
#     print('Ошибка подключения к базе данных')

# app = QApplication(sys.argv)
# win = Window()
# win.show()
# sys.exit(app.exec())
#!/usr/bin/python3
import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QLabel, QPushButton, QHBoxLayout, QMessageBox)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy
from bd_vhod import DatabaseConfigWindow
from PyQt5.QtWidgets import QApplication, QDialog
from config_manager import ConfigManager
from theme_manager import ThemeManager

from add_link import AddLinkWindow
from search_window import SearchWindow
from add_razdel import AddRazdel
from add_slovo import AddSlovo
from add_zakladki import AddZakladkiWindow
from regist import RegistrationWindow
from PyQt5.QtSql import QSqlDatabase
from check_add_bd import check_and_create_database


# def setup_database():
#     db = QSqlDatabase.addDatabase('QPSQL')
#     db.setHostName('localhost')
#     db.setDatabaseName('ssylki')
#     db.setPort(5432)
#     db.setUserName('postgres')
#     db.setPassword('123456')

#     if not db.open():
#         print('Ошибка подключения к базе данных')
#         return False
#     return True

class Window(QWidget):
    def __init__(self, id_polz=None, role=None, config_manager=None):
        super().__init__()
        self.id_polz = id_polz
        self.role = role
        self.config_manager = config_manager
        self.theme_manager = ThemeManager(config_manager) if config_manager else None
        
        self.setWindowTitle('Ссылки')
        self.setGeometry(300, 300, 1700, 1000)

        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().hide()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)

        self.top_panel_layout = QHBoxLayout()
        
        # Инициализация кнопок
        self.setup_buttons()

        self.main_layout.addLayout(self.top_panel_layout)
        self.main_layout.addWidget(self.table)
        self.setLayout(self.main_layout)

        self.load_data()

    def setup_buttons(self):
        while self.top_panel_layout.count():
            item = self.top_panel_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        #общие кнопки
        self.search_button = QPushButton('Поиск')
        self.search_button.clicked.connect(self.open_search_window)
        self.top_panel_layout.addWidget(self.search_button)
        
        self.theme_button = QPushButton('Сменить тему')
        self.theme_button.clicked.connect(self.toggle_theme)
        self.top_panel_layout.addWidget(self.theme_button)

        if self.role == 'admin':
            self.add_button = QPushButton('+ Добавить ссылку')
            self.add_razdel_btn = QPushButton('+ Добавить раздел')
            self.add_slovo_btn = QPushButton('+ Добавить ключевое слово')
            self.refresh_button = QPushButton('Обновить таблицу')
            
            self.add_button.clicked.connect(self.open_add_window)
            self.add_razdel_btn.clicked.connect(self.open_add_razdel)
            self.add_slovo_btn.clicked.connect(self.open_add_slovo)
            self.refresh_button.clicked.connect(self.load_data)

            self.top_panel_layout.addWidget(self.add_button)
            self.top_panel_layout.addWidget(self.add_razdel_btn)
            self.top_panel_layout.addWidget(self.add_slovo_btn)
            self.top_panel_layout.addWidget(self.refresh_button)

            self.zakladki_button = QPushButton('Добавить в закладки')
            self.zakladki_button.clicked.connect(self.open_zakladki_window)
            self.top_panel_layout.addWidget(self.zakladki_button)

        elif self.role == 'user':
            self.zakladki_button = QPushButton('Добавить в закладки')
            self.zakladki_button.clicked.connect(self.open_zakladki_window)
            self.top_panel_layout.addWidget(self.zakladki_button)

        else:
            self.reg_button = QPushButton('Зарегистрироваться')
            self.vhod_button = QPushButton('Вход')
            
            self.reg_button.clicked.connect(self.open_registration_window)
            self.vhod_button.clicked.connect(self.open_vhod_window)
            
            self.top_panel_layout.addStretch()
            self.top_panel_layout.addWidget(self.reg_button)
            self.top_panel_layout.addWidget(self.vhod_button)
            return

        self.top_panel_layout.addStretch()
        self.exit_button = QPushButton('Выход')
        self.exit_button.clicked.connect(self.logout)
        self.top_panel_layout.addWidget(self.exit_button)

    def update_role(self, id_polz, role):
        self.id_polz = id_polz
        self.role = role
        self.setup_buttons()
        self.load_data()

    def toggle_theme(self):
        if self.theme_manager:
            self.theme_manager.toggle_theme()

    def logout(self):
        self.id_polz = None
        self.role = None
        self.setup_buttons()
        self.load_data()
    
    def open_add_window(self):
        self.add_window = AddLinkWindow()
        self.add_window.show()
        self.add_window.destroyed.connect(self.load_data)

    def open_search_window(self):
        self.search_window = SearchWindow()
        self.search_window.show()

    def open_add_razdel(self):
        self.add_razdel = AddRazdel()
        self.add_razdel.show()
        self.add_razdel.destroyed.connect(self.load_data)

    def open_add_slovo(self):
        self.add_slovo_window = AddSlovo()
        self.add_slovo_window.show()
        self.add_slovo_window.destroyed.connect(self.load_data)

    def open_zakladki_window(self):
        if self.id_polz:
            self.zakladki_window = AddZakladkiWindow(self.id_polz)
            self.zakladki_window.show()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Необходимо войти в систему!')

    def open_registration_window(self):
        self.reg_window = RegistrationWindow()
        self.reg_window.show()

    def open_vhod_window(self):
        from vhod import VhodWindow
        self.vhod_window = VhodWindow(main_window=self)
        self.vhod_window.show()

    def load_data(self):
        self.table.setRowCount(0)
        q = QSqlQuery()
        
        if not QSqlDatabase.database().isOpen():
            QMessageBox.critical(self, 'Ошибка', 'Нет подключения к базе данных')
            return

        q.exec_('select naimen, ssylka, opisanie, skrinshot from ssylki_tab')

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Название', 'Ссылка', 'Описание', 'Снимок'])

        row = 0
        while q.next():
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(q.value(0))))
            self.table.setColumnWidth(0, 150)
            self.table.setItem(row, 1, QTableWidgetItem(str(q.value(1))))
            self.table.setColumnWidth(1, 180)
            self.table.setItem(row, 2, QTableWidgetItem(str(q.value(2))))
            self.table.setColumnWidth(2, 400)

            img_data = q.value(3)
            if img_data:
                pixmap = QPixmap()
                if pixmap.loadFromData(img_data):
                    pixmap = pixmap.scaled(680, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    label = QLabel()
                    label.setPixmap(pixmap)
                    label.setAlignment(Qt.AlignCenter)
                    self.table.setRowHeight(row, 300)
                    self.table.setColumnWidth(3, 700)
                    self.table.setCellWidget(row, 3, label)
                else:
                    self.table.setItem(row, 3, QTableWidgetItem('Ошибка конвертации'))
            else:
                self.table.setItem(row, 3, QTableWidgetItem('Нет данных'))
            row += 1

def setup_full_database(db_info):
    """Создаёт БД ssylki и все таблицы, если их нет"""
    
    # 1. Подключаемся к системной БД postgres
    setup_conn = QSqlDatabase.addDatabase('QPSQL', 'setup_connection')
    setup_conn.setHostName(db_info['host'])
    setup_conn.setDatabaseName('postgres')
    setup_conn.setPort(db_info['port'])
    setup_conn.setUserName(db_info['user'])
    setup_conn.setPassword(db_info['password'])
    
    if not setup_conn.open():
        QMessageBox.critical(None, 'Ошибка', 'Не удалось подключиться к серверу PostgreSQL')
        return False
    
    # 2. Проверяем, существует ли целевая БД
    q = QSqlQuery(setup_conn)
    target_db = db_info['db_name']
    q.exec_(f"SELECT 1 FROM pg_database WHERE datname = '{target_db}'")
    
    if not q.next():
        q.exec_(f"CREATE DATABASE {target_db}")
        print(f"База данных '{target_db}' создана.")
    
    setup_conn.close()
    QSqlDatabase.removeDatabase('setup_connection')
    
    # 3. Подключаемся к целевой БД ssylki
    db = QSqlDatabase.addDatabase('QPSQL')
    db.setHostName(db_info['host'])
    db.setDatabaseName(target_db)
    db.setPort(db_info['port'])
    db.setUserName(db_info['user'])
    db.setPassword(db_info['password'])
    
    if not db.open():
        QMessageBox.critical(None, 'Ошибка', f'Не удалось подключиться к базе данных {target_db}')
        return False
    
    # 4. Создаём таблицы
    return check_and_create_database(db)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    config_manager = ConfigManager("default")
    theme_manager = ThemeManager(config_manager)
    theme_manager.apply_theme()
    
    db_dialog = DatabaseConfigWindow("default")
    if db_dialog.exec_() != QDialog.Accepted:
        sys.exit(0)
        
    if not setup_full_database(db_dialog.db_info):
        QMessageBox.critical(None, 'Ошибка', 'Не удалось инициализировать базу данных.')
        sys.exit(1)
        
    win = Window(config_manager=config_manager) 
    win.show()
    sys.exit(app.exec())

# if __name__ == '__main__':
#     # if not setup_database():
#     #     sys.exit(1)
#     # app = QApplication(sys.argv)
#     app = QApplication(sys.argv)
#     db_dialog = DatabaseConfigWindow()
#     if db_dialog.exec_() != QDialog.Accepted:
#         sys.exit(0)  

#     db = QSqlDatabase.database()
#     if not check_and_create_database(db):
#         QMessageBox.critical(None, 'Ошибка', 'Не удалось создать таблицы в базе данных.')
#         sys.exit(1)

#     win = Window() 
#     win.show()
#     sys.exit(app.exec())
