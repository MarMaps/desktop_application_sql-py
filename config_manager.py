import os
import configparser
import sys


def get_program_dir():
    """Возвращает каталог, где находится программа"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def get_user_config_dir():
    """Возвращает каталог для конфигурационных файлов пользователя"""
    home = os.path.expanduser("~")
    config_dir = os.path.join(home, ".config", "links_app")
    os.makedirs(config_dir, exist_ok=True)
    return config_dir


def get_user_config_file(username):
    """Возвращает путь к конфигурационному файлу пользователя"""
    config_dir = get_user_config_dir()
    return os.path.join(config_dir, f"{username}.ini")


class ConfigManager:
    def __init__(self, username):
        self.username = username
        self.config_file = get_user_config_file(username)
        self.config = configparser.ConfigParser()
        self.load()

    def load(self):
        """Загружает конфигурацию из файла"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)

    def save(self):
        """Сохраняет конфигурацию в файл"""
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def set_db_connection(self, host, db_name, port, user, password):
        """Сохраняет данные подключения к БД"""
        if not self.config.has_section('database'):
            self.config.add_section('database')
        self.config.set('database', 'host', host)
        self.config.set('database', 'db_name', db_name)
        self.config.set('database', 'port', str(port))
        self.config.set('database', 'user', user)
        self.config.set('database', 'password', password)
        self.save()

    def get_db_connection(self):
        """Возвращает словарь с данными подключения к БД"""
        if not self.config.has_section('database'):
            return None
        return {
            'host': self.config.get('database', 'host'),
            'db_name': self.config.get('database', 'db_name'),
            'port': self.config.getint('database', 'port'),
            'user': self.config.get('database', 'user'),
            'password': self.config.get('database', 'password')
        }

    def has_db_connection(self):
        """Проверяет, сохранены ли данные подключения к БД"""
        return self.config.has_section('database')