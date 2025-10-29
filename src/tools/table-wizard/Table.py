class Table:
    def __init__(self, data=None, headers=None):
        if data:
            self.data = data
        else:
            self.data = []
        if headers:
            self.headers = headers
        else:
            self.headers = [""] * len(self.data)

    # Задать данные таблицы
    def set_data(self, data):
        self.data = data

    # Получить данные таблицы
    def get_data(self):
        return self.data

    # Получить заголовки таблицы
    def get_headers(self):
        return self.headers

    # Задать заголовки таблицы
    def set_headers(self, headers):
        self.headers = headers

    def has_headers(self):
        return bool(self.headers)

    # Добвать столбец в таблицу
    def add_column(self, column, header=""):
        self.headers.append(header)
        for i in range(len(self.data)):
            self.data[i].append(column[i])

    # Вставить столбец в таблицу
    def insert_column(self, index, column, header=""):
        self.headers.insert(index, header)
        for i in range(len(self.data)):
            self.data[i].insert(index, column[i])

    def delete_column(self, index):
        self.headers.pop(index)
        for i in range(len(self.data)):
            self.data.pop(index)

    # Добавить ряд в таблицу
    def add_row(self, row):
        self.data.append(row)

    # Вставить ряд в таблицу
    def insert_row(self, index, row):
        self.data.insert(index, row)

    # Удалить ряд из таблицы
    def delete_row(self, index):
        self.data.pop(index)

    # Получить ряд из таблицы
    def get_row(self, index):
        return self.data[index]

    # Получить размер таблицы
    def size(self):
        return (len(self.data), len(self.data[0]))

    def __len__(self):
        return self.size()
