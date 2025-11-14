import sys
from application import Application


def excepthook(ext_type, value, traceback):
    sys.__excepthook__(ext_type, value, traceback)
app = Application()
sys.excepthook = excepthook
if __name__ == '__main__':
    app.start()
