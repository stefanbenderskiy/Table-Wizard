import sys
from application import Application

app = Application()


def excepthook(ext_type, value, traceback):
    sys.__excepthook__(ext_type, value, traceback)


if __name__ == '__main__':
    app.start()
