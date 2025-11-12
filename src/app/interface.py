from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent

from src.app.appdata import AppData
from src.app.history import History, Action
from src.tools.tablewizard.Table import Table, TableOrderError, FilterType, InvalidFunctionFormat
from resources import Resources
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QWidget, \
    QInputDialog, QAbstractItemView
from PyQt6 import uic, QtCore


class CreateWindow(QWidget):
    def __init__(self, main_window):
        self.main_window = main_window
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.application = main_window.application
        self.load_ui()
        self.init_ui()

    def load_ui(self):
        try:
            uic.loadUi(Resources.get_ui("create-window.ui"), self)
        except Exception as e:
            self.application.logger.error("Failed to load window ui: " + str(e), sender="CREATE_WINDOW")

    def init_ui(self):
        self.cancel_button.clicked.connect(self.close)
        self.create_button.clicked.connect(self.create)
        self.location_change_button.clicked.connect(self.change_location)

    def change_location(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        filename = file_dialog.getExistingDirectory()
        self.location_edit.setText(filename)

    def create(self):
        name = self.name_edit.text()
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a name")
            return
        location = self.location_edit.text()
        if not location:
            QMessageBox.warning(self, "Warning", "Please enter a location")
            return
        rows = int(self.rows_edit.text())
        columns = int(self.columns_edit.text())
        headers = self.headers_edit.text().strip().split(', ')
        if len(headers) > columns:
            QMessageBox.critical("Error", "Too many headers")
            return
        elif len(headers) < columns:
            headers = headers + [['-'] * (len(headers) - columns)]
        try:
            print(headers)
            filename = f'{location}/{name}.csv'
            table = Table([(['-'] * rows) * columns], headers=headers)
            table.save(filename)
            self.main_window.load_table(filename)
            self.close()
        except Exception as e:
            raise e
            QMessageBox.critical(self, "Error", 'Invalid location!')
            self.application.logger.error("Failed to create table: " + str(e), sender="CREATE_WINDOW")


class OpenWindow(QWidget):
    def __init__(self, main_window):
        self.main_window = main_window
        super().__init__()
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.application = main_window.application
        self.load_ui()
        self.init_ui()

    def load_ui(self):
        try:
            uic.loadUi(Resources.get_ui("open-window.ui"), self)
        except Exception as e:
            self.application.logger.error("Failed to load window ui: " + str(e), sender="OPEN_WINDOW")

    def init_ui(self):
        self.tables = {}
        for name in AppData.get_all_tables():
            self.tables_list.addItem(name)
            self.tables[name] = AppData.get_table_path(name)

        self.tables_list.itemClicked.connect(self.select_table)
        self.open_button.clicked.connect(self.open_table)
        self.create_button.clicked.connect(self.create_table)

    def open_table(self):
        self.main_window.import_table()
        self.close()

    def select_table(self):
        if self.tables_list.selectedItems():
            name = self.tables_list.selectedItems()[0].text()
            path = self.tables[name]
            try:
                self.main_window.load_table(path)
                self.close()
            except Exception as e:
                QMessageBox.critical(self, "Error", 'File not found!')

    def create_table(self):
        self.main_window.create_table()
        self.close()


class OrderWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.application = main_window.application
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
        order_type = self.order_type_combo_box.currentText()
        keys = self.keys_edit.text().strip().split(",")
        reverse = self.reversed_check_box.isChecked()
        converter = None
        if order_type == "Auto":
            def convert(x):
                try:
                    return float(x)
                except Exception:
                    try:
                        return int(x)
                    except Exception:
                        return x

            converter = convert
        elif order_type == "Integer":
            converter = int
        elif order_type == "Float":
            converter = float
        elif order_type == "Lenght":
            converter = len
        elif order_type == "String":
            converter = str
        return converter, keys, reverse


class InsertWindow(QWidget):
    def __init__(self, window):
        super().__init__()
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
    def __init__(self, application):
        super().__init__()
        self.application = application
        self.load_ui()
        self.filename = ''
        self.history = History()
        resent_file = AppData.get_resent_file()
        if resent_file:
            try:
                self.load_table(resent_file)
            except Exception as e:
                self.table = Table()
                self.open_table()
        else:
            self.table = Table()
            self.open_table()
        self.init_ui()

    # Загрузка интерфейса из ui файла
    def load_ui(self):
        try:
            uic.loadUi(Resources.get_ui("main-window.ui"), self)
        except Exception as e:
            self.application.logger.error("Failed to load window ui: " + str(e), sender="MAIN_WINDOW")

    def init_ui(self):
        # Инициализация меню
        self.action_import.triggered.connect(self.import_table)
        self.action_open_table.triggered.connect(self.open_table)
        self.action_create.triggered.connect(self.create_table)
        self.action_save.triggered.connect(self.save_table)
        self.action_add_row.triggered.connect(self.add_row)
        self.action_add_column.triggered.connect(self.add_column)
        self.action_insert_row.triggered.connect(self.insert_row)
        self.action_insert_column.triggered.connect(self.insert_column)
        self.action_delete_row.triggered.connect(self.delete_row)
        self.action_delete_column.triggered.connect(self.delete_column)
        self.action_order_rows.triggered.connect(self.order_rows)
        self.action_order_columns.triggered.connect(self.order_columns)
        self.action_undo.triggered.connect(self.undo)
        self.action_redo.triggered.connect(self.redo)
        self.action_last.triggered.connect(self.last)

        # Иницализация редактора
        self.table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_widget.itemSelectionChanged.connect(self.display_selected_items)
        self.value_edit.editingFinished.connect(self.edit_selected_items)
        self.add_column_button.clicked.connect(self.add_column)
        self.add_row_button.clicked.connect(self.add_row)
        self.insert_row_button.clicked.connect(self.insert_row)
        self.insert_column_button.clicked.connect(self.insert_column)
        self.delete_column_button.clicked.connect(self.delete_column)
        self.delete_row_button.clicked.connect(self.delete_row)
        self.order_rows_button.clicked.connect(self.order_rows)
        self.order_columns_button.clicked.connect(self.order_columns)
        # Инициализация анализа
        self.select_button.clicked.connect(self.select)

    """ >>> Функции меню <<<"""

    def open_table(self):
        self.open_window = OpenWindow(self)
        self.open_window.show()

    def create_table(self):
        try:
            self.create_window = CreateWindow(self)
            self.create_window.show()
        except Exception as e:
            print(e)

    def load_table(self, filename):
        try:
            def load():
                self.filename = filename
                AppData.set_resent_file(filename)
                self.table = Table.load(filename)
                self.update_table()
                self.path_label.setText(f"Path: {filename}")
                self.history = History()
                self.apply_action("Load")

            if self.filename != '':
                id = QMessageBox.question(self, "Load new table", "Are you sure to load other table?")
                if id == 16384:
                    self.save_table()
                    load()
            else:
                load()
        except Exception as e:
            self.application.logger.error("Failed to load table: " + str(e), sender="MAIN_WINDOW")
            raise e

    def import_table(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        filename = file_dialog.getOpenFileName()[0]
        if filename:
            try:
                self.load_table(filename)
            except Exception as e:
                self.application.logger.error("Failed to import table: " + str(e), sender="MAIN_WINDOW")

    def save_table(self):
        if self.filename:
            try:
                self.table.save(self.filename)
                name = self.filename.split("/")[-1].split(".")[0]
                tables = AppData.get_all_tables()
                if name not in tables:
                    AppData.add_table(name, self.filename)
                else:
                    AppData.update_table(name, self.filename)
            except Exception as e:
                self.application.logger.error("Failed to save table: " + str(e), sender="MAIN_WINDOW")
                QMessageBox.critical(self, "Error", f"Failed to save table!")
        else:
            self.export_table()

    def export_table(self):
        file_dialog = QFileDialog()
        filename = file_dialog.getSaveFileName()[0]
        if filename:
            try:
                self.table.save(filename)
            except Exception as e:
                self.application.logger.error("Failed to save table: " + str(e), sender="MAIN_WINDOW")
                QMessageBox.critical(self, "Error", f"Failed to save table: Invalid filepath!")

    def last(self):
        self.table = self.history.last()
        self.update_table()

    def undo(self):
        self.history.undo()
        action = self.history.get_current_action()
        if action != None:
            self.table = Table.from_str(action.get_content())
            self.update_table()

    def redo(self):
        self.history.redo()
        action = self.history.get_current_action()
        if action != None:
            self.table = Table.from_str(action.get_content())
            self.update_table()

    """ >>> Функции редактора <<<"""

    # Отобразить выбранные элементы
    def display_selected_items(self):
        indexes = self.table_widget.selectedIndexes()
        rows = list(set(map(lambda x: x.row(), indexes)))
        columns = list(set(map(lambda x: x.column(), indexes)))
        self.selected_items = zip(rows, columns)
        try:
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
            self.selected_items_edit.setText(f"{columns_selection}; {rows_selection}")
            if len(indexes) == 1:
                self.value_edit.setText(indexes[0].data())
            else:
                self.value_edit.setText("...")
        except Exception as e:
            self.application.logger.error("Failed to display selected items: " + str(e), sender="MAIN_WINDOW")

    def edit_selected_items(self):
        value = self.value_edit.text()
        for i in self.table_widget.selectedIndexes():
            self.table.set_item(i.row(), i.column(), value)
        self.update_table()
        self.apply_action('Edit')

    def add_column(self):
        header, ok_pressed = QInputDialog.getText(self, "Add column", "Header:")
        if ok_pressed:
            self.table.add_column([""] * len(self.table), header)
            self.apply_action('Add column')
            self.update_table()

    def add_row(self):
        header, ok_pressed = QInputDialog.getText(self, "Add row", "Header:")
        if ok_pressed:
            self.table.add_row([header] + [""] * (self.table.size()[1] - 1), )
            self.apply_action('Add row')
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
                    self.apply_action('Insert row')
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
                    self.apply_action('Insert column')
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
                    self.apply_action('Delete column')
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
                    self.table.delete_row(int(index) - 1)
                    self.apply_action('Delete row')
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
            converter, keys, reverse = order_window.input()
            try:
                if keys == ['']:
                    keys = None
                else:
                    keys = list(map(lambda x: int(x) - 1, keys))
                try:
                    self.table.order_rows(keys, reverse, conventer=converter)
                    self.apply_action('Order rows')
                    self.update_table()
                except Exception:
                    QMessageBox.critical(self, "Error", f"Invalid keys or order type!")
            except Exception:
                QMessageBox.warning(self, "Warning",
                                    f"Key-columns should contain indexes of key-columns splited by comma!")
            order_window.close()

        order_window.order_button.clicked.connect(clicked)

    def order_columns(self):
        order_window = OrderWindow(self)
        order_window.setWindowTitle("Order columns")
        order_window.keys_label.setText("Key rows")
        order_window.show()

        def clicked():
            conventer, keys, reverse = order_window.input()
            try:
                if keys == ['']:
                    keys = None
                else:
                    keys = list(map(lambda x: int(x) - 1, keys))
                try:
                    self.table.order_columns(keys, reverse=reverse, conventer=conventer)
                    self.apply_action('Order columns')
                    self.update_table()
                except TableOrderError:
                    QMessageBox.critical(self, "Error", f"Keys have different type!")
                except Exception:
                    QMessageBox.critical(self, "Error", f"Invalid keys or order type!")

            except Exception:
                QMessageBox.warning(self, "Warning", f"Key-rows should contain indexes of key-rows splited by comma!")
            order_window.close()

        order_window.order_button.clicked.connect(clicked)

    def apply_action(self, name):
        try:
            self.history.add_action(Action(name, str(self.table)))
        except Exception as e:
            self.application.logger.error("Failed to add action:" + str(e), sender="MAIN_WINDOW")

    """Функции анализа"""

    def select(self):
        filter = self.filter_edit.text()
        filter_type = self.filter_type_combo_box.currentText()
        if filter_type == "Value":
            finding = self.table.find(filter)
        else:
            try:
                finding = self.table.find(filter, FilterType.Function)
            except InvalidFunctionFormat:
                QMessageBox.critical(self, 'Error', "Invalid filter function!")
                return
        result = ''
        for item in finding:
            value = item[0]
            pos = item[1]
            header = self.table.get_header(pos[1])
            text = f'<p><b>{header}:</b>{value} {(pos[0] + 1, pos[1] + 1)}</p>'
            result = result + text
        self.finding_browser.setHtml(result)

    def update_table(self):
        self.table_widget.setRowCount(self.table.size()[0])
        self.table_widget.setColumnCount(self.table.size()[1])
        self.table_widget.setHorizontalHeaderLabels(self.table.get_headers())
        for i, row in enumerate(self.table.get_rows()):
            for j, t in enumerate(row):
                item = QTableWidgetItem(t)
                self.table_widget.setItem(i, j, item)

    def closeEvent(self, event):
        if self.filename == '':
            id = QMessageBox.question(self, 'Exit without saving', 'Are you sure to exit without saving?')
            if id != 16384:
                self.show()
        else:
            self.save_table()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        modifiers = event.modifiers()
        if modifiers == (Qt.KeyboardModifier.AltModifier | Qt.KeyboardModifier.ControlModifier):
            if key == Qt.Key.Key_A:
                self.add_column()
            if key == Qt.Key.Key_I:
                self.insert_column()
            elif key == Qt.Key.Key_O:
                self.order_columns()
            elif key == Qt.Key.Key_D:
                self.delete_column()
        elif modifiers == (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier):
            if key == Qt.Key.Key_I:
                self.import_table()
            elif key == Qt.Key.Key_O:
                self.open_table()
            elif key == Qt.Key.Key_C:
                self.create()
        elif modifiers == (Qt.KeyboardModifier.ControlModifier):
            if key == Qt.Key.Key_Z:
                self.undo()
            elif key == Qt.Key.Key_Y:
                self.redo()
            elif key == Qt.Key.Key_I:
                self.insert_row()
            elif key == Qt.Key.Key_O:
                self.order_rows()
            elif key == Qt.Key.Key_D:
                self.delete_row()
            elif key == Qt.Key.Key_S:
                self.save_table()
            elif key == Qt.Key.Key_E:
                self.export_table()
            elif key == Qt.Key.Key_L:
                self.last()
