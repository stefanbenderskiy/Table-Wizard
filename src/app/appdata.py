from src.tools.database.database import DataBase


class AppData:
    database = DataBase("data/appdata.sqlite")

    @staticmethod
    def get_value(name):
        try:
            return AppData.database.get_request("""SELECT Value FROM Values WHERE Name = ?""", (name,))[0][0]
        except Exception:
            pass

    @staticmethod
    def set_value(name, value):
        try:
            AppData.database.set_request("""UPDATE Values SET Value = ? WHERE Name = ?""", (value, name))[0][0]
        except Exception:
            pass
    @staticmethod
    def get_values():
        return AppData.database.select("Values", "Value")
    @staticmethod
    def get_resent_file():
        return AppData.get_value("Resent file")

    @staticmethod
    def set_resent_file(filename):
        return AppData.set_value("Resent file",filename)
    @staticmethod
    def get_table_path(table_name):
        return AppData.database.select("Tables", "Path", "",table_name)[0][0]

    @staticmethod
    def add_table(table_name, path):
        AppData.database.set_request("""INSERT INTO Tables VALUES (?, ?)""", (table_name, path))
    @staticmethod
    def get_all_tables():
        return list(map(lambda x: x[0], AppData.database.get_request("""SELECT Name FROM Tables""",())))
