#!/usr/bin/python3

import sys #функции в ос
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication  # управление окнами, кнопками, меню^M
from PyQt5.QtSql import QSqlDatabase  # для подключения к БД^M
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import os


class Tb(QTableWidget):
    def __init__(self, wg):
        self.wg = wg  # запомнить окно, в котором эта таблица показывается
        super().__init__(wg)
        #self.row = -1
        self.setGeometry(10, 10, 500, 500)
        self.setColumnCount(4)
        self.verticalHeader().hide();
        self.updt() # обновить таблицу
        # запретить изменять поля
        self.setEditTriggers(QTableWidget.NoEditTriggers) 

# инициализация таблицы
    def updt(self):
        self.setRowCount(0);
        self.setHorizontalHeaderLabels(['Наименование', 'Ссылка', 'Описание', 'Скриншот']) # заголовки столцов
        
        # SQL запрос
        query = QSqlQuery()
        sql = """select naimen, ssylka, opisanie, skrinshot from ssylki_tab"""
        
        if query.exec_(sql):  # выполняем запрос
            row = 0
            while query.next():  # проходим по всем строкам результата
                self.insertRow(row)
                
                # Заполняем ячейки
                n_item = QTableWidgetItem(query.value(0))
                s_item = QTableWidgetItem(query.value(1))
                op_item = QTableWidgetItem(query.value(2))
                sk_item = QTableWidgetItem(query.value(3))
                
                self.setItem(row, 0, n_item)
                self.setItem(row, 1, s_item)
                self.setItem(row, 2, op_item)
                self.setItem(row, 3, sk_item)
                
                img_name = q.value(3)
                pixmap = pixmap.scaled(300,300)
				
                label = QLabel()
				label.setPixmap(pixmap)
				
				self.table.setRowHeight(row, 200)
				self.table.setColumnWidth(3, 300)
				self.table.setCellWidget(row, 3, label)
                
                row += 1
        else:
            print("Ошибка SQL:", query.lastError().text())





