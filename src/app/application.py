import sys
from src.tools.tablewizard.Table import Table
from database import DataBase
from main_window import MainWindow
from PyQt6.QtWidgets import QApplication
from src.app.logger import Logger


# Класс сборки приложения
class Application:
    # Старт приложения
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.logger =  Logger("../../log.txt")
        self.main_window = MainWindow(self)
    def start(self):
        self.main_window.show()
        sys.__excepthook__ = self.main_window.excepthook
        sys.exit(self.app.exec())
    # Остановка приложения
    def stop(self):
        self.app.quit()
    def get_database(self):
        return self.database
    # Получить главное окно приложения
    def get_main_window(self):
        return self.main_window

    def get_logger(self):
        return self.logger

app = Application()
if __name__ == '__main__':
    app.start()
