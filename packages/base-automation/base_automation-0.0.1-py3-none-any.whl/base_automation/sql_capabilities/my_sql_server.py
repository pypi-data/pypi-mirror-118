import mysql.connector
from base_automation import report


class MySqlServer:

    @report.step("initiate my sql_capabilities server connection")
    def __init__(self, user='root', password='password', host='127.0.0.1', database='sys'):
        self._connection = mysql.connector.connect(user=user, password=password,
                                                   host=host,
                                                   database=database)
        self._cursor = self._connection.cursor()
        self._data_result = None

    @report.step("get data")
    def get_data(self, query, close_connection=True):
        try:
            self._cursor.execute(query)
            self._data_result = list(self._cursor.fetchall())
            if close_connection:
                self.close_connection()
            return self._data_result
        except Exception as e:
            print(e)
            self.close_connection()
            assert False

    @report.step("insert data")
    def insert_data(self, query, data, is_tuple=True, close_connection=True):
        try:
            if is_tuple:
                self._cursor.executemany(query, data)
            else:
                self._cursor.execute(query, data)

            self._connection.commit()
            if close_connection:
                self.close_connection()
        except Exception as e:
            print(e)
            self.close_connection()
            assert False

    @report.step("close connection")
    def close_connection(self):
        try:
            self._connection.close()
        except Exception as e:
            print(e)
            assert False
