from enum import Enum


class InvalidTableFormat(Exception):
    pass


class TableOrderError(Exception):
    pass


class InvalidFilterType(Exception):
    pass


class InvalidFunctionFormat(Exception):
    pass


class FilterType(Enum):
    Value = 0
    Function = 1


class Filter:
    def __init__(self, value, type=FilterType.Value):
        self.value = value
        if type in [FilterType.Value, FilterType.Function]:
            self.type = type
        else:
            raise InvalidFilterType(f"Invalid filter type: {type}!")

    def filter(self, table):
        filtred_data = []
        if self.type == FilterType.Value:
            for row in range(len(table.get_data())):
                for column in range(len(table.get_row(row))):
                    item = table.get_item(row, column)
                    if self.value in item:
                        filtred_data.append((item, (row, column)))
        elif self.type == FilterType.Function:
            for row in range(len(table.get_data())):
                for column in range(len(table.get_row(row))):
                    x = table.get_item(row, column)
                    try:
                        flag = eval(self.value)
                        if flag:
                            filtred_data.append((x, (row, column)))
                    except Exception:
                        pass

        return filtred_data


class Table:
    def __init__(self, data=None, headers=None):
        if data:
            self.data = data
        else:
            self.data = []
        if headers:
            self.headers = headers
        else:
            self.headers = [""] * len(self.data) or []

    @staticmethod
    def load(filename):
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if lines == []:
                return Table()
            headers = lines[0].replace('\n', '').split(';')
            data = list(map(lambda x: x.replace('\n', '').split(';'), lines[1:]))
            table = Table(data, headers)
            return table

    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(str(self))

    @staticmethod
    def from_str(string):
        lines = list(filter(lambda x: x, string.split('\n')))
        headers = lines[0].split(';')
        data = list(map(lambda x: x.split(';'), lines[1:]))
        return Table(data, headers)

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def get_header(self, column):
        return self.headers[column]

    def get_headers(self):
        return self.headers

    def set_headers(self, headers):
        self.headers = headers

    def has_headers(self):
        return bool(self.headers)

    def add_column(self, column, header=""):
        self.headers.append(header)
        for i in range(len(self.data)):
            self.data[i].append(column[i])

    def insert_column(self, index, column, header=""):
        self.headers.insert(index, header)
        for i in range(len(self.data)):
            self.data[i].insert(index, column[i])

    def delete_column(self, index):
        self.headers.pop(index)
        for i in range(len(self.data)):
            self.data[i].pop(index)

    def order_columns(self, keys=None, reverse=False, conventer=None):
        columns = self.get_columns()
        if not keys:
            keys = list(range(len(self.data)))

        def key(x):
            values = []
            for k in keys:
                if conventer:
                    values.append(conventer(x[k]))
                else:
                    values.append(x[k])
            return tuple(values)

        try:
            ordered_columns = sorted(columns, reverse=reverse, key=key)
            self.data = [[ordered_columns[j][i] for j in range(len(self.headers))] for i in range(len(self.data))]
        except Exception:
            raise TableOrderError

    def get_column(self, column):
        return [i[column] for i in self.data]

    def get_columns(self):
        columns = []
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if i == 0:
                    columns.append([self.data[i][j]])
                else:
                    columns[j].append(self.data[i][j])
        return columns

    def add_row(self, row):
        self.data.append(row)

    def insert_row(self, index, row):
        self.data.insert(index, row)

    def order_rows(self, keys=None, reverse=False, conventer=None):
        rows = self.get_rows()
        if not keys:
            keys = list(range(len(self.headers)))

        def key(x):
            values = []
            for k in keys:
                if conventer:
                    values.append(conventer(x[k]))
                else:
                    values.append(x[k])
            return tuple(values)

        try:
            self.data = sorted(rows, reverse=reverse, key=key)
        except Exception:
            raise TableOrderError

    def delete_row(self, index):
        self.data.pop(index)

    def get_row(self, index):
        return self.data[index]

    def get_rows(self):
        return self.get_data()

    def get_item(self, row, column):
        return self.data[row][column]

    def set_item(self, row, column, value):
        self.data[row][column] = str(value)

    def find(self, filter):
        return filter.filter(self)

    # Получить размер таблицы
    def size(self):
        return (len(self.data), len(self.headers))

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return ";".join(self.headers) + "\n" + "\n".join([";".join(i) for i in self.data]) + "\n"
