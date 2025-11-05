import sys
from datetime import datetime

from src.tools.tablewizard.Table import Table
from resources import Resources
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, \
    QInputDialog
from PyQt6 import uic


class OrderWindow(QMainWindow):
    def __init__(self, window):
        super(OrderWindow, self).__init__(window)
        self.application = window.application
        self.load_ui()
        self.init_ui()

    def load_ui(self):
        try:
            uic.loadUi(Resources.get_ui("order-window.ui"), self)
        except Exception as e:
            self.application.logger.error("Failed to load window ui: " + str(e), sender="ORDER_WINDOW")

    def init_ui(self):
        self.setFixedSize(400, 200)
        self.cancel_button.clicked.connect(self.close)

    def input(self):
        return self.keys_edit.text().strip().split(","), self.reversed_check_box.isChecked()


class InsertWindow(QMainWindow):
    def __init__(self, window):
        super(InsertWindow, self).__init__(window)
        self.application = window.application
        self.load_ui()
        self.init_ui()

    def load_ui(self):
        try:
            uic.loadUi(Resources.get_ui("insert-window.ui"), self)
        except Exception as e:
            self.application.logger.error("Failed to load window ui: " + str(e), sender="INSERT_WINDOW")

    def init_ui(self):
        self.setFixedSize(400, 200)
        self.cancel_button.clicked.connect(self.close)

    def input(self):
        return self.index_edit.value(), self.header_edit.text()


class MainWindow(QMainWindow):
    def __init__(self, application, table=Table()):
        super().__init__()
        self.application = application
        self.table = table
        self.load_ui()
        self.init_ui()

    # Загрузка интерфейса из ui файла
    def load_ui(self):
        try:
            print("ПРОВЕРКА НА ОШИБКУ")
            uic.loadUi(Resources.get_ui("main-window.ui"), self)
            print("ОШИБКИ НЕТ")
        except Exception as e:
            print("ОШИБКА ЕСТЬ")
            self.application.logger.error("Failed to load window ui: " + str(e), sender="MAIN_WINDOW")

    def init_ui(self):
        # Инициализация меню
        self.action_open.triggered.connect(self.load_table)
        self.action_new.triggered.connect(self.new_table)
        self.action_save.triggered.connect(self.save_table)
        self.action_add_row.triggered.connect(self.add_row)
        self.action_add_column.triggered.connect(self.add_column)
        self.action_insert_row.triggered.connect(self.insert_row)
        self.action_insert_column.triggered.connect(self.insert_column)
        self.action_delete_row.triggered.connect(self.delete_row)
        self.action_delete_column.triggered.connect(self.delete_column)
        self.action_order_rows.triggered.connect(self.order_rows)
        self.action_order_columns.triggered.connect(self.order_сolumns)

        # Иницализация редактора
        self.table_widget.itemSelectionChanged.connect(self.display_selection)
        self.value_edit.textEdited.connect(self.edit_selection)
        self.add_column_button.clicked.connect(self.add_column)
        self.add_row_button.clicked.connect(self.add_row)
        self.insert_row_button.clicked.connect(self.insert_row)
        self.insert_column_button.clicked.connect(self.insert_column)
        self.delete_column_button.clicked.connect(self.delete_column)
        self.delete_row_button.clicked.connect(self.delete_row)
        self.order_rows_button.clicked.connect(self.order_rows)
        self.order_columns_button.clicked.connect(self.order_columns)

    """ >>> Функции меню <<<"""

    def new_table(self):
        window = MainWindow(self.application)
        window.show()

    def load_table(self):
        try:
            filename = QFileDialog.getOpenFileName()[0]
            self.table = Table.load(filename)
            self.path_label.setText(f"Path: {filename}")
        except Exception:
            pass
        self.update_table()

    def save_table(self, format="csv"):
        try:
            filename = QFileDialog.getSaveFileName()[0]
            self.table.save(filename)
        except Exception as e:
            self.application.logger.error("Failed to save table: " + str(e), sender="MAIN_WINDOW")
            QMessageBox.critical(self, "Error", f"Failed to save table. Error:\n {e.__class__.__name__}")

    """ >>> Функции редактора <<<"""

    # Отобразить выбранные элементы
    def display_selection(self):
        indexes = self.table_widget.selectedIndexes()
        rows = list(set(map(lambda x: x.row(), indexes)))
        columns = list(set(map(lambda x: x.column(), indexes)))
        self.selection = zip(rows, columns)
        columns_selection = ""
        rows_selection = ""
        if len(columns) == 1:
            columns_selection = str(columns[0] + 1)
        elif columns == list(range(columns[0], columns[-1] + 1)):
            columns_selection = f"{columns[0] + 1} - {columns[-1] + 1}"
        elif len(columns) < 5:
            columns_selection = ", ".join(map(lambda x: str(x + 1), columns))
        else:
            columns_selection = f"{columns[0] + 1}, ... {columns[-1] + 1}"
        if len(rows) == 1:
            rows_selection = str(rows[0] + 1)
        elif rows == list(range(rows[0], rows[-1] + 1)):
            rows_selection = f"{rows[0] + 1} - {rows[-1] + 1}"
        elif len(rows) < 5:
            rows_selection = ", ".join(map(lambda x: str(x + 1), rows))
        else:
            rows_selection = f"{rows[0] + 1}, ... {rows[-1] + 1}"
        self.columns_selected_label.setText(f"Columns selected: {columns_selection}")
        self.rows_selected_label.setText(f"Rows selected: {rows_selection}")
        self.selection_edit.setText(f"{columns_selection}; {rows_selection}")
        if len(indexes) == 1:
            self.value_edit.setText(indexes[0].data())
        else:
            self.value_edit.setText("...")

    def edit_selection(self):
        value = self.value_edit.text()
        for i in self.table_widget.selectedIndexes():
            item = QTableWidgetItem(value)
            self.table_widget.setItem(i.row(), i.column(), item)

    def add_column(self):
        header, ok_pressed = QInputDialog.getText(self, "Add column", "Header:")
        if ok_pressed:
            self.table.add_column([""] * len(self.table), header)
            self.update_table()

    def add_row(self):
        header, ok_pressed = QInputDialog.getText(self, "Add row", "Header:")
        if ok_pressed:
            self.table.add_row([header] + [""] * (self.table.size()[1] - 1), )
            self.update_table()

    def insert_row(self):
        insert_window = InsertWindow(self)
        insert_window.setWindowTitle("Insert row")
        insert_window.show()

        def clicked():
            index, header = insert_window.input()
            if index > 0:
                try:
                    self.table.insert_row(index - 1, [header] + [""] * (len(self.table) - 1))
                    self.update_table()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Invalid row index!")
            else:
                QMessageBox.warning(self, "Warning", f"Index should be greater than zero")
            insert_window.close()

        insert_window.insert_button.clicked.connect(clicked)

    def insert_column(self):
        insert_window = InsertWindow(self)
        insert_window.setWindowTitle("Insert column")
        insert_window.show()

        def clicked():
            index, header = insert_window.input()
            if index > 0:
                try:
                    self.table.insert_column(index - 1, [""] * self.table.size()[1], header)
                    self.update_table()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Invalid column index!")

            else:
                QMessageBox.warning(self, "Warning", f"Index should be greater than zero")
            insert_window.close()

        insert_window.insert_button.clicked.connect(clicked)

    def delete_column(self):
        index, ok_pressed = QInputDialog.getInt(self, "Delete column", "Column index:")
        if ok_pressed:
            try:
                if int(index) > 0:
                    self.table.delete_column(int(index) - 1)
                    self.update_table()
                else:
                    QMessageBox.warning(self, "Error", f"Index should be greater than zero")
            except Exception:
                QMessageBox.critical(self, "Error", f"Invalid column index!")

    def delete_row(self):
        index, ok_pressed = QInputDialog.getInt(self, "Delete row", "Row index:")
        if ok_pressed:
            try:
                if int(index) > 0:
                    self.table.delete_column(int(index) - 1)
                    self.update_table()
                else:
                    QMessageBox.warning(self, "Error", f"Index should be greater than zero")
            except Exception:
                QMessageBox.critical(self, "Error", f"Invalid row index!")

    def order_rows(self):
        order_window = OrderWindow(self)
        order_window.setWindowTitle("Order rows")
        order_window.keys_label.setText("Key columns")
        order_window.show()

        def clicked():
            keys, reverse = order_window.input()
            try:
                if keys == ['']:
                    keys = None
                else:
                    keys = list(map(lambda x: int(x) + 1, keys))
                try:
                    self.table.order_rows(keys, reverse)
                    self.update_table()
                except Exception:
                    QMessageBox.critical(self, "Error", f"Invalid keys!")
            except Exception:
                QMessageBox.warning(self, "Warning",
                                    f"Key-columns should contain indexes of key-columns splited by comma!")
            order_window.close()

        order_window.order_button.clicked.connect(clicked)

    def order_сolumns(self):
        order_window = OrderWindow(self)
        order_window.setWindowTitle("Order columns")
        order_window.keys_label.setText("Key rows")
        order_window.show()

        def clicked():
            keys, reverse = order_window.input()
            try:
                if keys == ['']:
                    keys = None
                else:
                    keys = list(map(lambda x: int(x) + 1, keys))
                try:
                    self.table.order_columns(keys, reverse)
                    self.update_table()
                except Exception:
                    QMessageBox.critical(self, "Error", f"Invalid keys!")
            except Exception:
                QMessageBox.warning(self, "Warning", f"Key-rows should contain indexes of key-rows splited by comma!")
            order_window.close()

        order_window.order_button.clicked.connect(clicked)

    def update_table(self):
        self.table_widget.setRowCount(self.table.size()[0])
        self.table_widget.setColumnCount(self.table.size()[1])
        self.table_widget.setHorizontalHeaderLabels(self.table.get_headers())
        for i, row in enumerate(self.table.get_rows()):
            for j, t in enumerate(row):
                item = QTableWidgetItem(t)
                self.table_widget.setItem(i, j, item)

    def excepthook(self, ext_type, value):
        sys.__excepthook__(ext_type, value)
