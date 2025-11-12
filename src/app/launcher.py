import sys
from application import Application
from src.app.appdata import AppData


def excepthook(ext_type, value, traceback):
    sys.__excepthook__(ext_type, value, traceback)
app = Application()
sys.excepthook = excepthook
AppData.clear()
if __name__ == '__main__':
    app.start()
