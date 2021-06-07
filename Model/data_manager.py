import sqlite3

from Model.UserClass import UserDetector


class Database:
    def __init__(self, link_to_data):
        self._conn = sqlite3.connect(link_to_data)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def get_all_user_name(self):
        result = self.query("""
        SELECT NAME FROM EMPLOYEE;
        """)
        my_data = [i[0] for i in result]
        # i[0] is NAME
        return my_data

    def get_load_infor(self):
        result = self.query("""
        SELECT * FROM EMPLOYEE
        ORDER BY UNIT;
        """)
        my_data = [i for i in result]
        # i[0] is NAME
        return my_data

    def insert_employee(self, employee):
        result = self.query(f'INSERT INTO EMPLOYEE VALUES ({employee.ID},{employee.name},{employee.sex},{employee.age},{employee.unit});')
        print(result)


with Database('Model/data/database/database.db') as db:
    # print(db.get_all_user_name())
    # print(db.get_load_infor())
    db.insert_employee(UserDetector('TEST001', 'PhuDinhTruong', 'MALE', 28, 'FREELANCER'))
