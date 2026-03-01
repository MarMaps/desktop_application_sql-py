from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, QMessageBox, QComboBox)
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtCore import Qt, QByteArray
import os

class AddLinkWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавить новую ссылку')
        self.setGeometry(400, 300, 500, 400)
        
        self.image_path = ""
        self.setup_ui()
        self.load_razdely()  # загружаем разделы при открытии окна
    
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
        layout.addWidget(self.description_input)

        # --- ВЫПАДАЮЩИЙ СПИСОК РАЗДЕЛОВ ---
        layout.addWidget(QLabel('Раздел:'))
        self.razdel_combo = QComboBox()
        layout.addWidget(self.razdel_combo)
        # ----------------------------------
        
        layout.addWidget(QLabel('Снимок экрана:'))
        
        file_layout = QHBoxLayout()
        self.file_label = QLabel('Файл не выбран')
        file_layout.addWidget(self.file_label)
        
        self.select_file_btn = QPushButton('Выбрать файл')
        self.select_file_btn.clicked.connect(self.select_image)
        file_layout.addWidget(self.select_file_btn)
        layout.addLayout(file_layout)
        
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
        # Читаем все разделы из таблицы razdely и добавляем в комбобокс
        query = QSqlQuery()
        query.exec_("SELECT id, razdel FROM razdely")
        
        while query.next():
            razdel_id = query.value(0)    # первый столбец — id
            razdel_name = query.value(1)  # второй столбец — razdel
            # добавляем текст (название) и прячем id внутри как "пользовательские данные"
            self.razdel_combo.addItem(razdel_name, razdel_id)
    
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

        # Получаем id выбранного раздела из комбобокса
        razdel_id = self.razdel_combo.currentData()

        with open(self.image_path, 'rb') as f:
            image_bytes = f.read()
        byte_array = QByteArray(image_bytes)

        # Шаг 1: сохраняем саму ссылку
        query = QSqlQuery()
        query.prepare("""INSERT INTO ssylki_tab (naimen, ssylka, opisanie, skrinshot) 
            VALUES (:name, :link, :desc, :img)""")
        
        query.bindValue(":name", name)
        query.bindValue(":link", link)
        query.bindValue(":desc", description)
        query.bindValue(":img", byte_array)
        
        if not query.exec_():
            QMessageBox.warning(self, 'Ошибка', 'Не удалось сохранить ссылку!')
            return

        # Шаг 2: узнаём id только что добавленной ссылки
        new_ssylka_id = query.lastInsertId()

        # Шаг 3: записываем в промежуточную таблицу связь раздел <-> ссылка
        query2 = QSqlQuery()
        query2.prepare("""INSERT INTO razdel_ssylka (id_razdela, id_ssylki) 
            VALUES (:id_razdela, :id_ssylki)""")
        
        query2.bindValue(":id_razdela", razdel_id)
        query2.bindValue(":id_ssylki", new_ssylka_id)
        
        if query2.exec_():
            QMessageBox.information(self, 'Успех', 'Данные сохранены!')
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Ссылка сохранена, но раздел не привязан!')