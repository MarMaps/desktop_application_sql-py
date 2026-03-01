#!/usr/bin/python3
import sys
import io
from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QPushButton, QHBoxLayout)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from add_link import AddLinkWindow 
from search_window import SearchWindow


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ссылки')
        self.setGeometry(300, 300, 1700, 1000)

        main_layout = QVBoxLayout()
        
        #кнопка добавления
        button_layout = QHBoxLayout()
        self.add_button = QPushButton('+ Добавить ссылку')
        self.add_button.clicked.connect(self.open_add_window)

        self.search_button = QPushButton('Поиск')
        self.search_button.clicked.connect(self.open_search_window)

        button_layout.addStretch()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.search_button)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        #cозд таблицы
        self.table = QTableWidget(self)
        main_layout.addWidget(self.table)
        
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.table.verticalHeader().hide()
        
        self.setLayout(main_layout)
        
        self.load_data()
    
    def open_add_window(self):
        self.add_window = AddLinkWindow()
        self.add_window.show()
        
        self.add_window.destroyed.connect(self.load_data) #не работает
    
    def open_search_window(self):
        self.search_window = SearchWindow()
        self.search_window.show()

    def load_data(self):
        self.table.setRowCount(0)
        
        q = QSqlQuery()
        q.exec_('SELECT naimen, ssylka, opisanie, skrinshot FROM ssylki_tab')
        
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
            #self.table.setColumnHeight(2, 100)

            img_data = q.value(3)
            
            if img_data:
                pixmap = QPixmap()
                if pixmap.loadFromData(img_data):
                    pixmap = pixmap.scaled(600, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)               
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

db = QSqlDatabase.addDatabase('QPSQL')
db.setHostName('localhost')
db.setDatabaseName('ssylki')
db.setPort(5432)
db.setUserName('postgres')
db.setPassword('123456')

if not db.open():
    print('Ошибка подключения к базе данных')


app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())