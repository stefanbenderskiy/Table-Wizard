import sys
from resources import Resources
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui()
        self.init_ui()
    def load_ui(self):
        try:
            uic.loadUi(Resources.get_resource("ui","main.ui"),self)
        except Exception as e:
            pass
    def init_ui(self):
        pass

    def excepthook(self, ext_type, value):
        sys.__excepthook__(ext_type, value)

            
