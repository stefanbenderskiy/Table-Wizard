import sqlite3


class DataBase:
    def __init__(self, db_name):
        self.name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def query(self, sql, params=None):
        return self.cursor.execute(sql, params)

    def commit(self):
        self.connection.commit()
    def get_request(self, sql, params=None):
        try:
            return self.query(sql, params).fetchall()
        except Exception as e:
            print(e)
    def set_request(self, sql, params=None):
        try:
            self.query(sql, params)
            self.commit()
        except Exception as e:
            print(e)
    def select(self):
        pass
    def get_all_data(self):
        return self.cursor.fetchall()
