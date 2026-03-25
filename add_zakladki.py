from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QComboBox, QMessageBox, QScrollArea, QCheckBox)
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtCore import Qt


class AddZakladkiWindow(QWidget):
    def __init__(self, id_polz):
        super().__init__()
        self.id_polz = id_polz
        self.setWindowTitle('Добавить в закладки')
        self.setGeometry(400, 300, 400, 300)

        self.checkboxes = []
        self.setup_ui()
        self.load_ssylki()

    def setup_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel('Выберите ссылки для добавления в закладки:'))

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll)

        buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton('Добавить')
        self.save_btn.clicked.connect(self.save_zakladki)
        buttons_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton('Отмена')
        self.cancel_btn.clicked.connect(self.close)
        buttons_layout.addWidget(self.cancel_btn)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def load_ssylki(self):
        query = QSqlQuery()
        query.exec_("select id, naimen, ssylka from ssylki_tab order by naimen")

        for cb in self.checkboxes:
            cb.deleteLater()
        self.checkboxes = []
        self.ids = []

        while query.next():
            ssylka_id = query.value(0)
            ssylka_name = query.value(1)
            ssylka_url = query.value(2)

            cb = QCheckBox(f'{ssylka_name} ({ssylka_url})')
            self.scroll_layout.addWidget(cb)
            self.checkboxes.append(cb)
            self.ids.append(ssylka_id)

        self.scroll_layout.addStretch()

    def save_zakladki(self):
        selected_count = 0

        for i, cb in enumerate(self.checkboxes):
            if cb.isChecked():
                ssylka_id = self.ids[i]

                query = QSqlQuery()
                query.prepare("""insert into zakladki (id_polz, id_ssylka)
                    values (:id_polz, :id_ssylka)""")
                query.bindValue(":id_polz", self.id_polz)
                query.bindValue(":id_ssylka", ssylka_id)

                if query.exec_():
                    selected_count += 1

        if selected_count > 0:
            QMessageBox.information(self, 'Успех', f'Добавлено в закладки: {selected_count}')
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Выберите хотя бы одну ссылку!')
