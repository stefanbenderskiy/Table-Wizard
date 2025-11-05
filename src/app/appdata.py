from src.tools.database.database import DataBase


class AppData:
    def __init__(self):
        self.database = DataBase("/data/appdata.sqlite")
    def get_value(self, name):
        select =  self.database.select("Values","Value",name, indificator="Name")
        return select[0][0]
    def set_value(self, name, value):
        pass
    def get_resent_file(self):
        return self.get_value("Resent file")
    def get_history(self):
        return self.get_value("History")
