import sys

from PyQt6.QtCore import QModelIndex
from PyQt6.QtGui import QAction

from src.tools.tablewizard.Table import Table
from resources import Resources
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QTableWidget
from PyQt6 import uic


class MainWindow(QMainWindow):
    def __init__(self, application, table):
        super().__init__()
        self.application = application
        self.table = None
        self.load_ui()
        self.init_ui()

    def load_ui(self):
        try:
            uic.loadUi(Resources.get_resource("ui", "main.ui"), self)
        except Exception as e:
            self.application.logger.error("Failed to load window ui: " + str(e), sender="MAIN_WINDOW")

    def update_editor(self):
        self.editor_table_widget.setRowCount(self.table.size()[0])
        self.editor_table_widget.setColumnCount(self.table.size()[1])
        self.editor_table_widget.setHorizontalHeaderLabels(self.table.get_headers())
        for i, row in enumerate(self.table.get_rows()):
            for j, t in enumerate(row):
                item = QTableWidgetItem(t)
                self.editor_table_widget.setItem(i, j, item)

    def items_selected(self):
        rows = list(set(map(lambda x: x.row(), self.editor_table_widget.selectedIndexes())))
        columns = list(set(map(lambda x: x.column(), self.editor_table_widget.selectedIndexes())))
        columns_selection = ""
        rows_selection = ""
        if len(columns) == 1:
            columns_selection = str(columns[0] + 1)
        elif columns == list(range(columns[0], columns[-1] + 1)):
            columns_selection = f"{columns[0] + 1} - {columns[-1] + 1}"
        elif len(columns) < 5:
            columns_selection = ", ".join(map(lambda x: str(x + 1),columns))
        else:
            columns_selection = f"{columns[0] + 1}, ... {columns[-1] + 1}"
        if len(rows) == 1:
            rows_selection = str(rows[0] + 1)
        elif rows == list(range(rows[0], rows[-1] + 1)):
            rows_selection = f"{rows[0] + 1} - {rows[-1] + 1}"
        elif len(rows) < 5:
            rows_selection = ", ".join(map(lambda x: str(x + 1),rows))
        else:
            rows_selection = f"{rows[0] + 1}, ... {rows[-1] + 1}"
        self.columns_selected_label.setText(f"Columns selected: {columns_selection}")
        self.rows_selected_label.setText(f"Rows selected: {rows_selection}")
        self.selection_label.setText(f"Selection:{columns_selection}; {rows_selection}")

    def init_ui(self):
        def init_menu():
            self.action_open.triggered.connect(self.load_table)
            self.action_new.triggered.connect(self.new_table)
            self.action_save.triggered.connect(self.save_table)

        def init_editor():
            self.editor_table_widget.itemSelectionChanged.connect(self.items_selected)

        init_menu()
        init_editor()

    def excepthook(self, ext_type, value):
        sys.__excepthook__(ext_type, value)

    def new_table(self):
        pass

    def load_table(self):
        try:
            filename = QFileDialog.getOpenFileName()[0]
            self.table = Table.load(filename)
            self.path_label.setText(f"Path: {filename}")
        except Exception as e:
            self.application.logger.error("Failed to load table: " + str(e), sender="MAIN_WINDOW")
            QMessageBox.critical(self, "Error", f"Failed to load table. Error:\n {e.__class__.__name__}")
        self.update_editor()

    def save_table(self, format="csv"):
        try:
            filename = QFileDialog.getSaveFileName()[0]
            self.table.save(filename)
        except Exception as e:
            self.application.logger.error("Failed to save table: " + str(e), sender="MAIN_WINDOW")
            QMessageBox.critical(self, "Error", f"Failed to save table. Error:\n {e.__class__.__name__}")
