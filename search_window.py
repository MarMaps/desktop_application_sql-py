from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QStackedWidget)
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Поиск ссылок')
        self.setGeometry(300, 200, 1400, 700)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        btn_layout = QHBoxLayout()

        self.btn_by_name = QPushButton('По названию сайта')
        self.btn_by_link = QPushButton('По ссылке')
        self.btn_by_razdel = QPushButton('По разделу')
        self.btn_by_slova = QPushButton('По ключевым словам')

        self.btn_by_name.clicked.connect(lambda: self.show_search_panel(0))
        self.btn_by_link.clicked.connect(lambda: self.show_search_panel(1))
        self.btn_by_razdel.clicked.connect(lambda: self.show_search_panel(2))
        self.btn_by_slova.clicked.connect(lambda: self.show_search_panel(3))

        btn_layout.addWidget(self.btn_by_name)
        btn_layout.addWidget(self.btn_by_link)
        btn_layout.addWidget(self.btn_by_razdel)
        btn_layout.addWidget(self.btn_by_slova)

        layout.addLayout(btn_layout)

        self.stack = QStackedWidget()

        #поиск по названию
        page_name = QWidget()
        p0 = QHBoxLayout()
        p0.addWidget(QLabel('Название сайта:'))
        self.input_name = QLineEdit()
        p0.addWidget(self.input_name)
        find_btn0 = QPushButton('Найти')
        find_btn0.clicked.connect(self.search_by_name)
        p0.addWidget(find_btn0)
        page_name.setLayout(p0)

        # поиск по ссылке
        page_link = QWidget()
        p1 = QHBoxLayout()
        p1.addWidget(QLabel('Ссылка:'))
        self.input_link = QLineEdit()
        p1.addWidget(self.input_link)
        find_btn1 = QPushButton('Найти')
        find_btn1.clicked.connect(self.search_by_link)
        p1.addWidget(find_btn1)
        page_link.setLayout(p1)

        # поиск по разделу (список)
        page_razdel = QWidget()
        p2 = QHBoxLayout()
        p2.addWidget(QLabel('Раздел:'))
        self.combo_razdel = QComboBox()
        self.load_razdely()
        p2.addWidget(self.combo_razdel)
        find_btn2 = QPushButton('Найти')
        find_btn2.clicked.connect(self.search_by_razdel)
        p2.addWidget(find_btn2)
        page_razdel.setLayout(p2)

        #поиск по словам
        page_slova = QWidget()
        p3 = QHBoxLayout()
        p3.addWidget(QLabel('Ключевое слово: '))
        self.input_slova = QLineEdit() 
        p3.addWidget(self.input_slova)
        find_btn3 = QPushButton('Найти')
        find_btn3.clicked.connect(self.search_by_slova)
        p3.addWidget(find_btn3)
        page_slova.setLayout(p3)

        self.stack.addWidget(page_name)    # индекс 0
        self.stack.addWidget(page_link)    # индекс 1
        self.stack.addWidget(page_razdel)  # индекс 2
        self.stack.addWidget(page_slova)  # индекс 3

        layout.addWidget(self.stack)

        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().hide()
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.show_search_panel(0)

    def show_search_panel(self, index):
        self.stack.setCurrentIndex(index)
        self.table.setRowCount(0)

    def load_razdely(self):
        query = QSqlQuery()
        query.exec_("select id, razdel from razdely")
        while query.next():
            self.combo_razdel.addItem(query.value(1), query.value(0))

    def search_by_name(self):
        text = self.input_name.text().strip()
        query = QSqlQuery()
        query.prepare("select naimen, ssylka, opisanie, skrinshot from ssylki_tab where naimen ilike :val")
        query.bindValue(":val", f"%{text}%")
        query.exec_()
        self.fill_table(query)

    def search_by_link(self):
        text = self.input_link.text().strip()
        query = QSqlQuery()
        query.prepare("select naimen, ssylka, opisanie, skrinshot from ssylki_tab WHERE ssylka ilike :val")
        query.bindValue(":val", f"%{text}%")
        query.exec_()
        self.fill_table(query)

    def search_by_razdel(self):
        razdel_id = self.combo_razdel.currentData()
        query = QSqlQuery()
        query.prepare("""select s.naimen, s.ssylka, s.opisanie, s.skrinshot from ssylki_tab s
            join razdel_ssylka rs on rs.id_ssylki = s.id
            where rs.id_razdela = :razdel_id""")
        query.bindValue(":razdel_id", razdel_id)
        query.exec_()
        self.fill_table(query)

    def search_by_slova(self):
        text = self.input_slova.text().strip()
        query = QSqlQuery()
        query.prepare("""
            SELECT s.naimen, s.ssylka, s.opisanie, s.skrinshot 
            FROM ssylki_tab s
            JOIN cluch_slova_ssylka cs_s ON cs_s.id_ssylka = s.id
            JOIN cluch_slova cs ON cs.id = cs_s.id_cluch_slova
            WHERE cs.slovo ILIKE :val""")
        query.bindValue(":val", f"%{text}%")
        query.exec_()
        self.fill_table(query)


    def fill_table(self, query):
        
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Название', 'Ссылка', 'Описание', 'Снимок'])
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 180)
        self.table.setColumnWidth(2, 400)

        row = 0
        while query.next():
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(query.value(0))))
            self.table.setItem(row, 1, QTableWidgetItem(str(query.value(1))))
            self.table.setItem(row, 2, QTableWidgetItem(str(query.value(2))))

            img_data = query.value(3)
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