import sqlite3
from getmac import get_mac_address
import socket
import subprocess
import os
COMMA = "'"


class DataBaseTable:
    global COMMA

    def __init__(self, file_name, table_name, table_columns: tuple):
        self.connection = sqlite3.connect(file_name)
        self.cursor = self.connection.cursor()
        self.name = table_name
        self.columns = table_columns

    def build_table(self):
        # cur.execute('CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real)')
        command = "CREATE TABLE {} ({} {}".format(self.name, self.columns[0][0], self.columns[0][1])
        self.columns = list(self.columns)
        first = self.columns.pop(0)
        self.columns = tuple(self.columns)

        for column in self.columns:
            command = command + ", {} {}".format(column[0], column[1])

        command += ")"
        self.columns = list(self.columns)
        self.columns.insert(0, first)

        self.columns = tuple(self.columns)
        self.cursor.execute(command)
        self.connection.commit()

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

        self.cursor.execute(command)
        self.connection.commit()

    def select(self, column: str, value: str):
        # cur.execute("SELECT * FROM stocks WHERE trans=?", ('BUY',))
        command = "SELECT * FROM {} WHERE {}={}".format(self.name, column, value)
        self.cursor.execute(command)
        return self.cursor.fetchall()

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

        self.cursor.execute(command)
        return self.cursor.fetchall()

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

        self.cursor.execute(command)
        self.connection.commit()


def test(to_return: bool):
    if to_return:
        return 1
    else:
        print('worked')


def main():
    print(os.getcwd())
    l = os.listdir()
    print(l)
    print(os.path.isdir(l[10]))
    os.chdir(l[6])
    l2 = os.getcwd()
    to = l2.split('\\')
    print(l2)
    subprocess.check_output('attrib')
    file = 'S dfgdfdfdfd HR'
    if 'S' or 'H' or 'R' in file:
        print('eys')


if __name__ == '__main__':
    main()

