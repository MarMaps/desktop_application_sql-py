import sys
import io
from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QLabel, QPushButton, QHBoxLayout)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from add_link import AddLinkWindow
from search_window import SearchWindow
from add_razdel import AddRazdel
from add_slovo import AddSlovo
from PyQt5.QtWidgets import QSizePolicy
from regist import RegistrationWindow
from add_zakladki import AddZakladkiWindow

class Window(QWidget):
    def __init__(self, id_polz):
        super().__init__()
        self.id_polz = id_polz
        self.setWindowTitle('Ссылки')
        self.setGeometry(300, 300, 1700, 1000)

        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().hide()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignTop)

        top_panel_layout = QHBoxLayout()
        self.add_button = QPushButton('+ Добавить ссылку')
        self.add_razdel = QPushButton('+ Добавить раздел')
        self.add_slovo = QPushButton('+ Добавить ключевое слово')
        self.search_button = QPushButton('Поиск')
        self.zakladki_button = QPushButton('Добавить в закладки')
        self.refresh_button = QPushButton('Обновить таблицу')
        self.exit_button = QPushButton('Выход')

        top_panel_layout.addWidget(self.add_button)
        top_panel_layout.addWidget(self.add_razdel)
        top_panel_layout.addWidget(self.add_slovo)
        top_panel_layout.addWidget(self.search_button)
        top_panel_layout.addWidget(self.refresh_button)
        top_panel_layout.addStretch()
        top_panel_layout.addWidget(self.zakladki_button)
        top_panel_layout.addWidget(self.exit_button)

        self.exit_button.clicked.connect(self.close)
        self.main_layout.addLayout(top_panel_layout)
        self.main_layout.addWidget(self.table)
        self.setLayout(self.main_layout)

        self.zakladki_button.clicked.connect(self.open_zakladki_window)
        self.add_button.clicked.connect(self.open_add_window)
        self.search_button.clicked.connect(self.open_search_window)
        self.add_razdel.clicked.connect(self.open_add_razdel)
        self.add_slovo.clicked.connect(self.open_add_slovo)
        self.refresh_button.clicked.connect(self.load_data)
        #self.reg_button.clicked.connect(self.open_registration_window)
        #self.vhod_button.clicked.connect(self.open_vhod_window)

        self.load_data()
    
    def open_add_window(self):
        self.add_window = AddLinkWindow()
        self.add_window.show()
        self.add_window.destroyed.connect(self.load_data)

    def open_search_window(self):
        self.search_window = SearchWindow()
        self.search_window.show()

    def open_zakladki_window(self):
        self.zakladki_window = AddZakladkiWindow(self.id_polz)
        self.zakladki_window.show()
    
    def open_add_razdel(self):
        self.add_razdel = AddRazdel()
        self.add_razdel.show()
        self.add_razdel.destroyed.connect(self.load_data)

    def open_add_slovo(self):
        self.add_slovo_window = AddSlovo()
        self.add_slovo_window.show()
        self.add_slovo_window.destroyed.connect(self.load_data)

    def open_registration_window(self):
        self.reg_window = RegistrationWindow()
        self.reg_window.show()

    def open_vhod_window(self):
        self.vhod_window = VhodWindow()
        self.vhod_window.show()

    def load_data(self):
        self.table.setRowCount(0)
        q = QSqlQuery()
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