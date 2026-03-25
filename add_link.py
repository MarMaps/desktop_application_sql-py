from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, 
                             QPushButton, QFileDialog, QMessageBox, QComboBox, QScrollArea, 
                             QCheckBox)
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtWidgets import QSizePolicy
import os

class AddLinkWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить новую ссылку')
        self.setGeometry(400, 300, 600, 500)

        self.image_path = ""
        self.checkboxes = []  
        self.setup_ui()
        self.load_razdely()
        self.load_slova()

    def setup_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel('Название сайта:'))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel('Ссылка:'))
        self.link_input = QLineEdit()
        layout.addWidget(self.link_input)

        layout.addWidget(QLabel('Описание:'))
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(80)
        layout.addWidget(self.description_input)

        layout.addWidget(QLabel('Раздел:'))
        self.razdel_combo = QComboBox()
        layout.addWidget(self.razdel_combo)

        layout.addWidget(QLabel('Ключевые слова:'))        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setMaximumHeight(120)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll)

        # Снимок экрана
        layout.addWidget(QLabel('Снимок экрана:'))

        file_layout = QHBoxLayout()
        self.file_label = QLabel('Файл не выбран')
        self.file_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        file_layout.addWidget(self.file_label)

        self.select_file_btn = QPushButton('Выбрать файл')
        self.select_file_btn.clicked.connect(self.select_image)
        file_layout.addWidget(self.select_file_btn)
        layout.addLayout(file_layout)

        # Кнопки
        buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton('Сохранить')
        self.save_btn.clicked.connect(self.save_data)
        buttons_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton('Отмена')
        self.cancel_btn.clicked.connect(self.close)
        buttons_layout.addWidget(self.cancel_btn)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def load_razdely(self):
        query = QSqlQuery()
        query.exec_("select id, razdel from razdely")

        while query.next():
            razdel_id = query.value(0)
            razdel_name = query.value(1)
            self.razdel_combo.addItem(razdel_name, razdel_id)

    def load_slova(self):
        query = QSqlQuery()
        query.exec_("select id, slovo from cluch_slova order by slovo")

        for cb in self.checkboxes:
            cb.deleteLater()
        self.checkboxes = []

        while query.next():
            slovo_id = query.value(0)
            slovo_name = query.value(1)
            
            cb = QCheckBox(slovo_name)
            cb.setProperty('id', slovo_id)
            self.scroll_layout.addWidget(cb)
            self.checkboxes.append(cb)

        self.scroll_layout.addStretch()

    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, 'Выберите изображение', '', 'Images (*.png *.jpg *.jpeg *.bmp *.gif)')

        if file_name:
            self.image_path = file_name
            self.file_label.setText(os.path.basename(file_name))
            self.file_label.setStyleSheet('color: green;')

    def save_data(self):
        name = self.name_input.text().strip()
        link = self.link_input.text().strip()
        description = self.description_input.toPlainText().strip()

        if not self.image_path:
            QMessageBox.warning(self, 'Ошибка', 'Выберите изображение!')
            return

        razdel_id = self.razdel_combo.currentData()

        with open(self.image_path, 'rb') as f:
            image_bytes = f.read()
        byte_array = QByteArray(image_bytes)

        query = QSqlQuery()
        query.prepare("""insert into ssylki_tab (naimen, ssylka, opisanie, skrinshot)
            values (:name, :link, :desc, :img)""")

        query.bindValue(":name", name)
        query.bindValue(":link", link)
        query.bindValue(":desc", description)
        query.bindValue(":img", byte_array)

        if not query.exec_():
            QMessageBox.warning(self, 'Ошибка', 'Не удалось сохранить ссылку!')
            return

        new_ssylka_id = query.lastInsertId()

        query2 = QSqlQuery()
        query2.prepare("""insert into razdel_ssylka (id_razdela, id_ssylki)
            values (:id_razdela, :id_ssylki)""")

        query2.bindValue(":id_razdela", razdel_id)
        query2.bindValue(":id_ssylki", new_ssylka_id)

        if not query2.exec_():
            QMessageBox.warning(self, 'Ошибка', 'Ссылка сохранена, но раздел не привязан!')
            return

        for cb in self.checkboxes:
            if cb.isChecked():
                slovo_id = cb.property('id')
                
                query3 = QSqlQuery()
                query3.prepare("""insert into cluch_slova_ssylka (id_ssylka, id_cluch_slova)
                    values (:id_ssylka, :id_cluch_slova)""")

                query3.bindValue(":id_ssylka", new_ssylka_id)
                query3.bindValue(":id_cluch_slova", slovo_id)

                if not query3.exec_():
                    QMessageBox.warning(self, 'Ошибка', 'Не удалось привязать ключевое слово!')

        QMessageBox.information(self, 'Успех', 'Данные сохранены!')
        self.close()
