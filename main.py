#!/usr/bin/python3

import sys #функции в ос
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication  # управление окнами, кнопками, меню^M
from PyQt5.QtSql import QSqlDatabase  # для подключения к БД^M
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QTableWidget
import tb_ssylki


class mainw(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(1000, 1000, 1000, 1000)
        self.setWindowTitle('QMainWindow')
        ok = self.con('localhost', 'ssylki', 5432, 'postgres', '123456')
        if not ok:
           print('Ошибка соединения')
        #tb = tb_ssylki.Tb(self)
        self.tb = tb_ssylki.Tb(self)  # сохраняем ссылку на таблицу
        self.setCentralWidget(self.tb)  # добавляем таблицу в главное окно

    def con(self, h, db1, pr, us, ps):
        db = QSqlDatabase.addDatabase('QPSQL')
        db.setHostName(h)
        db.setDatabaseName(db1)
        db.setPort(pr)
        db.setUserName(us)
        db.setPassword(ps)
        return db.open()



app = QApplication(sys.argv)

wq = mainw()
wq.show()
sys.exit(app.exec())


