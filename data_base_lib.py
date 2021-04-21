import sqlite3
from threading import Lock
from util.UtilConstants import UtilConstants
import os

location = os.getcwd()
location = location.split('\\')
if location[-1] != 'FinalProject':
    location.pop(-1)

location = '\\'.join(location)

UtilConstants.DATA_BASES_PATH = location + '\\DataBases'

COMMA = "'"


def default():
    print('d')


class DataBaseTable:
    global COMMA

    def __init__(self, file_name, table_name, table_columns: tuple):
        file_path = UtilConstants.DATA_BASES_PATH + '\\' + file_name
        self.connection = sqlite3.connect(file_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.name = table_name
        self.columns = table_columns
        self.lock = Lock()

    def build_table(self):
        # cur.execute('CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)')
        command = "CREATE TABLE IF NOT EXISTS {} ({} {}".format(self.name, self.columns[0][0], self.columns[0][1])
        self.columns = list(self.columns)
        first = self.columns.pop(0)
        self.columns = tuple(self.columns)

        for column in self.columns:
            command = command + ", {} {}".format(column[0], column[1])

        command += ")"

        # return popped value back to columns tuple:
        self.columns = list(self.columns)
        self.columns.insert(0, first)
        self.columns = tuple(self.columns)

        self.use_cursor_edit(command)

        # if table already exist than drop it:
        # self.delete_table()

    def add_row(self, values: list):
        # cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
        command = "INSERT INTO {} VALUES (".format(self.name)
        if type(values[0]) == str or type(values[0]) == chr:
            command = command + COMMA + values[0] + COMMA
        else:
            command = command + str(values[0])

        values.pop(0)

        for value in values:
            command = command + ","
            if type(value) == str or type(value) == chr:
                command = command + COMMA + value + COMMA
            else:
                command = command + str(value)

        command = command + ")"

        self.use_cursor_edit(command)

    def select(self, column: str, value: str):
        # cur.execute("SELECT * FROM stocks WHERE trans=?", ('BUY',))
        if type(value) == str:
            value = COMMA + value + COMMA

        command = "SELECT * FROM {} WHERE {}={}".format(self.name, column, value)
        data = self.use_cursor_select(command)
        return data

    def select_all(self):
        command = "SELECT * FROM {}".format(self.name)
        data = self.use_cursor_select(command)
        print(data)
        return data

    # values format: ((column, value), (column, value))
    def specific_select_by_two_columns(self, values: tuple):
        tuple_arg_1 = values[0]
        tuple_arg_2 = values[1]
        arg1 = ''
        arg2 = ''

        if type(tuple_arg_1[1]) == str:
            arg1 = COMMA + tuple_arg_1[1] + COMMA
        else:
            arg1 = str(tuple_arg_1[1])

        if type(tuple_arg_2[1]) == str:
            arg2 = COMMA + tuple_arg_2[1] + COMMA
        else:
            arg2 = str(tuple_arg_2[1])

        command = 'SELECT * FROM {} WHERE {}={} AND {}={}'.format(self.name, tuple_arg_1[0], arg1, tuple_arg_2[0], arg2)

        data = self.use_cursor_select(command)
        return data

    def update(self, value_to_update: tuple, client_to_update: tuple):
        arg1 = ''
        arg2 = ''

        if type(value_to_update[1]) == str:
            arg1 = COMMA + value_to_update[1] + COMMA
        else:
            arg1 = str(value_to_update[1])

        if type(client_to_update[1]) == str:
            arg2 = COMMA + client_to_update[1] + COMMA
        else:
            arg2 = str(client_to_update[1])

        command = 'UPDATE {} SET {} = {} WHERE {} = {}'\
            .format(self.name, value_to_update[0], arg1, client_to_update[0], arg2)

        self.use_cursor_edit(command)

    def delete_table(self):
        command = 'DROP TABLE IF EXISTS {}'.format(self.name)
        self.use_cursor_edit(command)

    def use_cursor_edit(self, command):
        self.lock.acquire()
        # print('ACQUIRE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        self.cursor.execute(command)
        self.connection.commit()

        self.lock.release()
        # print('RELEASE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    def use_cursor_select(self, command):
        self.lock.acquire(True)
        # print('ACQUIRE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        self.cursor.execute(command)
        data = self.cursor.fetchall()

        self.lock.release()
        # print('RELEASE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        return data


