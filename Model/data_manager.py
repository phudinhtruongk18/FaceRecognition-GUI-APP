import sqlite3
from datetime import datetime

from Model.ClassForSoftware import Employee, Session


class DataManager:
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

    def get_all_user_ID(self):
        result = self.query("""
        SELECT ID FROM EMPLOYEE;
        """)
        my_data = [i[0] for i in result]
        # i[0] is ID
        return my_data

    def get_load_infor(self):
        result = self.query("""
        SELECT * FROM EMPLOYEE
        ORDER BY UNIT;
        """)
        return result

    def insert_employee(self, employee):
        try:
            self.execute('INSERT INTO EMPLOYEE (ID, NAME, SEX, AGE, UNIT) VALUES (?, ?, ?, ?, ?)',
                         (employee.ID, employee.name, employee.sex, employee.age, employee.unit))
            # check = self.query('SELECT * FROM EMPLOYEE WHERE ID =?', (employee.ID,))
            # if check == employ -> return true
            return True
        except sqlite3.IntegrityError:
            print("IntegrityError")
        except Exception as e:
            print(e)
        return False

    def insert_session(self, session):
        try:
            self.execute('INSERT INTO SESSION (ID, NAME, DURATION) VALUES (?, ?, ?)',
                         (session.ID, session.name, session.duration))
            # check = self.query('SELECT * FROM EMPLOYEE WHERE ID =?', (employee.ID,))
            # if check == employ -> return true
            return True
        except sqlite3.IntegrityError:
            print("IntegrityError")
        except Exception as e:
            print(e)
        return False

    def insert_list_id_employee_to_saved_id_session(self, list_id_employee, id_session):
        try:
            for temp_id in list_id_employee:
                self.execute('INSERT INTO SAVED_SESSION (ID_EMPLOYEE, ID_SESSION) VALUES (?, ?)',
                             (temp_id, id_session))
            return True
        except sqlite3.IntegrityError:
            print("IntegrityError")
        except Exception as e:
            print(e)
        return False

    def get_all_session(self):
        sql = "SELECT * FROM SESSION"
        return self.query(sql)

    def get_all_employee_id_by_session_ID(self, ID_SESSION):
        sql = F"SELECT ID_EMPLOYEE FROM SAVED_SESSION WHERE ID_SESSION = ?;"
        result = self.query(sql, (ID_SESSION,))
        my_data = [i[0] for i in result]
        # i[0] is ID of the employee
        return my_data

    def get_all_employee_by_session_ID(self, ID_SESSION):
        sql = F"SELECT * FROM EMPLOYEE WHERE ID IN (SELECT ID_EMPLOYEE FROM SAVED_SESSION WHERE ID_SESSION = ?);"
        result = self.query(sql, (ID_SESSION,))
        return result

    def get_duration_by_session_ID(self, ID_SESSION):
        sql = F"SELECT DURATION FROM SESSION WHERE ID= ?;"
        result = self.query(sql, (ID_SESSION,))
        if result:
            return result[0][0]
        return result

    def get_all_employee_name_by_session_ID(self, ID_SESSION):
        sql = F"SELECT NAME FROM EMPLOYEE WHERE ID IN (SELECT ID_EMPLOYEE FROM SAVED_SESSION WHERE ID_SESSION = ?)"
        result = self.query(sql, (ID_SESSION,))
        my_data = [i[0] for i in result]
        # i[0] is ID of the employee
        return my_data

    def insert_and_get_id_recorder(self, ID_SESSION):
        try:
            now = datetime.now()
            ID_RECORDER = now.strftime('%Y-%m-%d %H:%M:%S')
            self.execute('INSERT INTO RECORDER (ID,ID_SESSION) VALUES (?, ?)',
                         (ID_RECORDER, ID_SESSION))
            # check = self.query('SELECT * FROM EMPLOYEE WHERE ID =?', (employee.ID,))
            # if check == employ -> return true
            return ID_RECORDER
        except sqlite3.IntegrityError:
            print("IntegrityError")
        except Exception as e:
            print(e)
        return None

    def insert_new_record(self, IS_BACKUP, ID_EMPLOYEE, ID_RECORDER):
        try:
            ARRIVED_TIME = datetime.now().strftime('%H:%M:%S')
            ARRIVED_TIME_RETURN = datetime.now().strftime('%Hh%Mm%S')

            self.execute("INSERT INTO DETAIL_RECORD (ARRIVED_TIME,IS_BACKUP,ID_EMPLOYEE,ID_RECORDER) VALUES (?,?,?,?)",
                         (ARRIVED_TIME, int(IS_BACKUP), ID_EMPLOYEE, ID_RECORDER))
            return ARRIVED_TIME_RETURN
        except sqlite3.IntegrityError:
            print("IntegrityError")
        except Exception as e:
            print(e)
        return None

    def get_all_recorder(self):
        sql = "SELECT ID FROM RECORDER;"
        result = self.query(sql)
        my_data = [i[0] for i in result]
        # i[0] is ID of the employee
        return my_data

    def get_recorder_by_time(self, begin_time, end_time):
        sql = "SELECT ID FROM RECORDER WHERE RECORD_DATE BETWEEN ? AND ?;"
        result = self.query(sql, (begin_time, end_time))
        my_data = [i[0] for i in result]
        # i[0] is ID of the employee
        return my_data

    def get_all_detail_record_by_recorder_id(self, ID_RECORDER):
        sql = "SELECT * FROM DETAIL_RECORD WHERE ID_RECORDER =?;"
        result = self.query(sql, (ID_RECORDER,))
        # i[0] is ID of the employee
        return result

    def delete_employee_by_id(self, ID_EMPLOYEE):
        try:
            sql = "DELETE FROM EMPLOYEE WHERE ID=?;"
            self.execute(sql, (ID_EMPLOYEE,))
            # i[0] is ID of the employee
            return True
        except sqlite3.Error as e:
            print(e)
        return False

    def delete_session_by_id(self, ID_SESSION):
        try:
            sql = "DELETE FROM SESSION WHERE ID=?;"
            self.execute(sql, (ID_SESSION,))
            sql2 = "DELETE FROM SAVED_SESSION WHERE ID_SESSION=?;"
            self.execute(sql2, (ID_SESSION,))
            return True
        except sqlite3.Error as e:
            print(e)
        return False

    def get_employee_infor_by_id(self, ID_EMPLOYEE):
        sql = "SELECT * FROM EMPLOYEE WHERE ID = ?;"
        result = self.query(sql, (ID_EMPLOYEE,))
        if not result:
            return None
        # return detail about employee instead array with 1 index
        return result[0]

    def get_state_of_employee(self, ID_RECORDER, ID_EMPLOYEE):
        sql = "SELECT * FROM DETAIL_RECORD WHERE ID_RECORDER = ? AND ID_EMPLOYEE = ?;"
        result = self.query(sql, (ID_RECORDER, ID_EMPLOYEE))
        print(result)
        print(result.__len__(), "<- len")
        len_of_list = result.__len__()
        return len_of_list

    def get_list_to_export(self, ID_RECORDER):
        sql = f"""
                SELECT A.ID,A.NAME,A.UNIT,B.ARRIVED_TIME, B.IS_BACKUP
                FROM DETAIL_RECORD AS B,EMPLOYEE AS A
                WHERE 
                A.ID = B.ID_EMPLOYEE AND 
                B.ID_RECORDER = ?
                ORDER BY B.ARRIVED_TIME;
                """
        result = self.query(sql, (ID_RECORDER,))
        return result

    def update_employee_infor_by_id(self, ID_EMPLOYEE, **kwargs):
        change_employee = self.get_employee_infor_by_id(ID_EMPLOYEE)
        if not change_employee:
            return None
        employee_to_change = Employee(*change_employee)

        # ID = kwargs.pop('ID', employee_to_change.ID)
        NAME = kwargs.pop('NAME', employee_to_change.name)
        SEX = kwargs.pop('SEX', employee_to_change.sex)
        AGE = kwargs.pop('AGE', employee_to_change.age)
        UNIT = kwargs.pop('UNIT', employee_to_change.unit)

        try:
            sql = "UPDATE EMPLOYEE SET NAME = ?, SEX = ?,AGE = ?, UNIT = ? WHERE ID=?;"
            self.execute(sql, (NAME, SEX, AGE, UNIT, ID_EMPLOYEE))
            return True
        except sqlite3.Error as e:
            print(e)
        return False

    def get_employee_to_export_by_time(self, TIMEBEGIN, TIMEEND):
        sql = f"""
            SELECT A.ID,A.NAME,A.UNIT,ALL_SESSION_TO_GO.ALL_SESSION , IFNULL(OFF.NOT_GO_TO_WORK,0) AS "OFF_WORK", ALL_SESSION_TO_GO.ALL_SESSION - IFNULL(OFF.NOT_GO_TO_WORK,0) AS "GO_TO_WORK"
            FROM 			
                EMPLOYEE AS A,
                (		
            
                        SELECT LIST_RECORD.ID_EMPLOYEE,count(LIST_RECORD.ID) AS "ALL_SESSION"
                        FROM (
                            SELECT B.*,A.ID_EMPLOYEE, A.ID_SESSION AS "confirm" FROM 
                            RECORDER AS B, SAVED_SESSION AS A
                        WHERE B.ID IN (SELECT RECORDER.ID FROM RECORDER WHERE RECORDER.ID BETWEEN ? AND ?)
                            AND B.ID_SESSION = A.ID_SESSION
                        ) AS LIST_RECORD
                        GROUP BY 
                            LIST_RECORD.ID_EMPLOYEE
                
                ) AS ALL_SESSION_TO_GO
            
            LEFT JOIN
                        (
                        
                        SELECT EXPORT.ID_EMPLOYEE, COUNT(*) AS "NOT_GO_TO_WORK"
                        FROM
                        (SELECT B.*,A.ID_EMPLOYEE FROM 
                            RECORDER AS B, SAVED_SESSION AS A
                        WHERE B.ID IN (SELECT RECORDER.ID FROM RECORDER WHERE RECORDER.ID BETWEEN ? AND ?)
                            AND B.ID_SESSION = A.ID_SESSION ) AS EXPORT
                        LEFT JOIN 
                        DETAIL_RECORD AS B
                            ON B.ID_RECORDER=EXPORT.ID
                            AND B.ID_EMPLOYEE = EXPORT.ID_EMPLOYEE
                        WHERE B.IS_BACKUP IS NULL
                        GROUP BY EXPORT.ID_EMPLOYEE
            
                    )AS OFF
            
            ON ALL_SESSION_TO_GO.ID_EMPLOYEE = OFF.ID_EMPLOYEE
            WHERE ALL_SESSION_TO_GO.ID_EMPLOYEE = A.ID                
            """
        result = self.query(sql, (TIMEBEGIN, TIMEEND, TIMEBEGIN, TIMEEND))
        return result

    def get_employee_did_not_go_to_work(self, ID_RECORDER):
        sql = f"""
    SELECT ALL_EMPLOYEE.* FROM 
        (SELECT D.ID,D.NAME,UNIT
        FROM RECORDER AS C,SAVED_SESSION AS A, EMPLOYEE AS D
        WHERE 
        C.ID = "2021-06-12 23:11:08"
        AND D.ID = A.ID_EMPLOYEE
        AND A.ID_SESSION = C.ID_SESSION) AS ALL_EMPLOYEE
    WHERE ALL_EMPLOYEE.ID NOT IN 
            (SELECT B.ID_EMPLOYEE 
            FROM DETAIL_RECORD AS B 
            WHERE B.ID_RECORDER = ?)
    ORDER BY ALL_EMPLOYEE.ID;
            """
        result = self.query(sql, (ID_RECORDER,))
        return result

# with Database('Model/data/database/database.db') as db:
# print(db.get_all_user_name())

# print(db.get_load_infor())

# if db.insert_employee(UserDetector('TEST002', 'Phu Dinh', 'MALE', 28, 'FREELANCER')):
#     print("Done")
# else:
#     print("Can't add this employee! Try Again")

# if db.insert_session(Session("TEST002","TEST NEK BN ƠI",69)):
#     print("Done")
# else:
#     print("Can't add this employee! Try Again")

# # RECORDER
# ID_SESSION = "TEST_SESSION_001"
# ID_RECORDER = db.insert_and_get_id_recorder(ID_SESSION)
# if result is not None:
#     print(ID_RECORDER)
#     print("Success")
# else:
#     print("Some thing Wrong when create new recorder")

# ADD NEW RECORD
# IS_BACKUP = True
# ID_EMPLOYEE = "ARAM001"
# ID_RECORDER = "THANKLONG001"
# if db.insert_new_record(IS_BACKUP, ID_EMPLOYEE, ID_RECORDER):
#     print(ID_RECORDER)
#     print("Success")
# else:
#     print("Some thing Wrong when create new recorder")

# print(db.get_all_recorder())
# my_recorder = db.get_recorder_by_time(begin_time="2019-02-20",end_time="2022-02-28")
# for temp2 in db.get_all_detail_record_by_recorder_id(my_recorder[0]):
#     thanklong = RecordDetail(temp2[0], temp2[1], temp2[2], temp2[3], temp2[4])
#     print(thanklong.id_recorder)

# delete
# db.insert_employee(UserDetector('TEST002', 'Phu Dinh', 'MALE', 28, 'FREELANCER'))
# if db.delete_employee_by_id('TEST002'):
#     print("Success")
# else:
#     print("Something went wrong! Try again")

# db.update_employee_infor_by_id(ID_EMPLOYEE="ARAM017",NAME="Phu Dinh",AGE=21,UNIT="FREELANCER")
# print(db.get_employee_infor_by_id("ARAM017"))
