from src.app.database import DataBase


class AppData:
    database = DataBase("data/appdata.sqlite")

    @staticmethod
    def get_value(name):
        try:
            return AppData.database.get_request("""SELECT Value FROM Dataset WHERE Name = ?""", (name,))[0][0]
        except Exception:
            return None

    @staticmethod
    def set_value(name, value):
        try:
            AppData.database.set_request("""UPDATE Dataset SET Value = ? WHERE Name = ?""", (value, name))
        except Exception:
            pass

    @staticmethod
    def get_values():
        data = AppData.get_value("""SELECT * FROM Dataset""")
        values = {}
        for i in data:
            values[i[0]] = i[1]
        return values

    @staticmethod
    def get_resent_file():
        return AppData.get_value("Resent file")

    @staticmethod
    def set_resent_file(filename):
        return AppData.set_value("Resent file", filename)

    @staticmethod
    def get_table_path(table_name):
        try:
            return AppData.database.get_request("""SELECT Path FROM Tables WHERE Name = ?""", (table_name,))[0][0]
        except Exception:
            return None

    @staticmethod
    def add_table(table_name, path):
        try:
            n = len(AppData.get_all_tables()) + 1
            AppData.database.set_request("""INSERT INTO Tables VALUES (?,?, ?)""", (n, table_name, path))
        except Exception:
            pass

    @staticmethod
    def update_table(table_name, path):
        try:
            AppData.database.set_request("""UPDATE Tables SET Path = ? WHERE Name = ?""", (path, table_name))
        except Exception:
            pass

    @staticmethod
    def get_all_tables():
        data = AppData.database.get_request("""SELECT Name FROM Tables""")
        if data:
            return list(map(lambda x: x[0], data))
        else:
            return []

    @staticmethod
    def clear_all_tables():
        try:
            AppData.database.set_request("""DELETE FROM Tables""")
        except Exception:
            pass

    @staticmethod
    def clear():
        AppData.clear_all_tables()
        AppData.set_resent_file('')
