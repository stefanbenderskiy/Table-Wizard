import sys
from application import Application

app = Application()


def excepthook(ext_type, value):
    sys.__excepthook__(ext_type, value)


if __name__ == '__main__':
    app.start()
