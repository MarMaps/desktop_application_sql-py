from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QLineEdit, QPushButton, QTableWidget, 
                              QTableWidgetItem, QComboBox, QStackedWidget)
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

        # --- КНОПКИ ВЫБОРА ТИПА ПОИСКА ---
        btn_layout = QHBoxLayout()

        self.btn_by_name = QPushButton('По названию сайта')
        self.btn_by_link = QPushButton('По ссылке')
        self.btn_by_razdel = QPushButton('По разделу')

        self.btn_by_name.clicked.connect(lambda: self.show_search_panel(0))
        self.btn_by_link.clicked.connect(lambda: self.show_search_panel(1))
        self.btn_by_razdel.clicked.connect(lambda: self.show_search_panel(2))

        btn_layout.addWidget(self.btn_by_name)
        btn_layout.addWidget(self.btn_by_link)
        btn_layout.addWidget(self.btn_by_razdel)
        layout.addLayout(btn_layout)

        # --- ПАНЕЛИ ВВОДА (переключаются через QStackedWidget) ---
        # QStackedWidget — это как стопка страниц, показывается только одна
        self.stack = QStackedWidget()

        # Страница 0 — поиск по названию
        page_name = QWidget()
        p0 = QHBoxLayout()
        p0.addWidget(QLabel('Название сайта:'))
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText('Введите название...')
        p0.addWidget(self.input_name)
        find_btn0 = QPushButton('Найти')
        find_btn0.clicked.connect(self.search_by_name)
        p0.addWidget(find_btn0)
        page_name.setLayout(p0)

        # Страница 1 — поиск по ссылке
        page_link = QWidget()
        p1 = QHBoxLayout()
        p1.addWidget(QLabel('Ссылка:'))
        self.input_link = QLineEdit()
        self.input_link.setPlaceholderText('Введите часть ссылки...')
        p1.addWidget(self.input_link)
        find_btn1 = QPushButton('Найти')
        find_btn1.clicked.connect(self.search_by_link)
        p1.addWidget(find_btn1)
        page_link.setLayout(p1)

        # Страница 2 — поиск по разделу (выпадающий список)
        page_razdel = QWidget()
        p2 = QHBoxLayout()
        p2.addWidget(QLabel('Раздел:'))
        self.combo_razdel = QComboBox()
        self.load_razdely()  # заполняем список разделов из БД
        p2.addWidget(self.combo_razdel)
        find_btn2 = QPushButton('Найти')
        find_btn2.clicked.connect(self.search_by_razdel)
        p2.addWidget(find_btn2)
        page_razdel.setLayout(p2)

        self.stack.addWidget(page_name)    # индекс 0
        self.stack.addWidget(page_link)    # индекс 1
        self.stack.addWidget(page_razdel)  # индекс 2

        layout.addWidget(self.stack)

        # --- ТАБЛИЦА РЕЗУЛЬТАТОВ ---
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().hide()
        layout.addWidget(self.table)

        self.setLayout(layout)

        # По умолчанию показываем первую панель
        self.show_search_panel(0)

    def show_search_panel(self, index):
        # Переключаем страницу в стеке
        self.stack.setCurrentIndex(index)
        # Очищаем таблицу при смене типа поиска
        self.table.setRowCount(0)

    def load_razdely(self):
        query = QSqlQuery()
        query.exec_("SELECT id, razdel FROM razdely")
        while query.next():
            self.combo_razdel.addItem(query.value(1), query.value(0))

    # --- МЕТОДЫ ПОИСКА ---

    def search_by_name(self):
        text = self.input_name.text().strip()
        query = QSqlQuery()
        query.prepare("SELECT naimen, ssylka, opisanie, skrinshot FROM ssylki_tab WHERE naimen ILIKE :val")
        query.bindValue(":val", f"%{text}%")
        query.exec_()
        self.fill_table(query)

    def search_by_link(self):
        text = self.input_link.text().strip()
        query = QSqlQuery()
        query.prepare("SELECT naimen, ssylka, opisanie, skrinshot FROM ssylki_tab WHERE ssylka ILIKE :val")
        query.bindValue(":val", f"%{text}%")
        query.exec_()
        self.fill_table(query)

    def search_by_razdel(self):
        razdel_id = self.combo_razdel.currentData()
        query = QSqlQuery()
        # Джойним через промежуточную таблицу
        query.prepare("""
            SELECT s.naimen, s.ssylka, s.opisanie, s.skrinshot 
            FROM ssylki_tab s
            JOIN razdel_ssylka rs ON rs.id_ssylki = s.id
            WHERE rs.id_razdela = :razdel_id
        """)
        query.bindValue(":razdel_id", razdel_id)
        query.exec_()
        self.fill_table(query)

    def fill_table(self, query):
        # Этот метод одинаково заполняет таблицу для любого типа поиска
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