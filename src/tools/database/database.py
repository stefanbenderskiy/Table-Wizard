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
    def select(self, table, column = None, item = None, indificator = "id"):
        if column:
            if item:
                return self.get_request("""SELECT ? FROM ? WHERE ? = ?""", (column,table,indificator, item))
            else:
                return self.get_request("""SELECT ? FROM ? WHERE ? = ?""", (column,table, indificator, item))
        else:
            return self.get_request("""SELECT * FROM ?""", (table,))
    def update(self, table, column, value, item = None, indificator = "id"):
        if item:
            self.set_request("""UPDATE ? SET ? = ?""", (table, column, value))
        else:
            self.set_request("""UPDATE ? SET ? = ? WHERE ? = ?""", (table, column,value, indificator, item))
    def insert(self, table, column, value, item, indificator = "id"):
        self.set_request("""INSERT INTO ?(?, ?) VALUES(?, ?)""",(table, indificator, column, item, value))

    def get_all_data(self):
        return self.cursor.fetchall()
