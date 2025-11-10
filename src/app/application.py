import sys

from src.app.appdata import AppData
from src.app.interface import MainWindow, OpenWindow
from PyQt6.QtWidgets import QApplication
from src.app.logger import Logger


# Класс сборки приложения
class Application:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.logger = Logger("log.txt")
        self.main_window = MainWindow(self)

    # Старт приложения
    def start(self):
        self.main_window.show()
        sys.exit(self.app.exec())

    # Остановка приложения
    def stop(self):
        self.app.quit()
    # Получить журнал приложения
    def get_logger(self):
        return self.logger
