import sys
from src.tools.tablewizard.Table import Table
from resources import Resources
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QTableWidget, QLineEdit, \
    QInputDialog, QComboBox
from PyQt6 import uic


class MainWindow(QMainWindow):
    def __init__(self, application, table = Table()):
        super().__init__()
        self.application = application
        self.table = table
        self.load_ui()
        self.init_ui()

    def load_ui(self):
        try:
            uic.loadUi(Resources.get_ui("main.ui"), self)
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

    def apply_style(self):
        with open(Resources.get_style("main-style.css"), "r", encoding='utf-8') as css_style:
            self.setStyleSheet(css_style.read())

    def items_selected(self):
        indexes = self.editor_table_widget.selectedIndexes()
        rows = list(set(map(lambda x: x.row(), indexes)))
        columns = list(set(map(lambda x: x.column(), indexes)))
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

    def edit_selected_items(self):
        value = self.value_edit.text()
        for i in self.editor_table_widget.selectedIndexes():
            item = QTableWidgetItem(value)
            self.editor_table_widget.setItem(i.row(), i.column(), item)

    def add_column(self):
        header, ok_pressed = QInputDialog.getText(self, "Add column", "Header:")
        if ok_pressed:
            self.table.add_column([""] * len(self.table), header)
            self.update_editor()

    def add_row(self):
        header, ok_pressed = QInputDialog.getText(self, "Add column", "Header:")
        if ok_pressed:
            self.table.add_row([header] + [""] * (self.table.size()[1] - 1), )
            self.update_editor()
    def delete_column(self):
        index, ok_pressed = QInputDialog.getInt(self, "Delete column", "Column index:")
        if ok_pressed:
            try:
                if int(index) > 0:
                    self.table.delete_column(int(index) - 1)
                    self.update_editor()
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
                    self.update_editor()
                else:
                    QMessageBox.warning(self, "Error", f"Index should be greater than zero")
            except Exception:
                QMessageBox.critical(self, "Error", f"Invalid row index!")

    def init_ui(self):
        def init_menu():
            self.action_open.triggered.connect(self.load_table)
            self.action_new.triggered.connect(self.new_table)
            self.action_save.triggered.connect(self.save_table)

        def init_editor():
            self.editor_table_widget.itemSelectionChanged.connect(self.items_selected)
            self.value_edit.textEdited.connect(self.edit_selected_items)
            self.add_column_button.clicked.connect(self.add_column)
            self.add_row_button.clicked.connect(self.add_row)
            self.delete_column_button.clicked.connect(self.delete_column)

        self.apply_style()
        init_menu()
        init_editor()

    def excepthook(self, ext_type, value):
        sys.__excepthook__(ext_type, value)

    def new_table(self):
        window  = MainWindow(self.application)

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
