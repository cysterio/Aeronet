import mysql.connector as db
from Utils.Credentials.CredUtils import Credentials
from datetime import datetime

class Schedule:
    ScheduleDB = db.connect(
        user="root", 
        password=Credentials.get_password(),
        host="localhost",
        database="Aeronet"
    )

    cursor = ScheduleDB.cursor()

    @staticmethod
    def dep_time(fno: str, dep_time: str = "") -> str:
        def fetch(fno: str) -> str:
            Schedule.cursor.execute(f'SELECT dep_time FROM Schedule WHERE flight_no = "{fno}" ')
            return Schedule.cursor.fetchone()[0]

        def update(fno: str, dep_time: str) -> None:
            Schedule.cursor.execute(f'UPDATE Schedule SET dep_time = "{dep_time}" WHERE flight_no = "{fno}" ')
            Schedule.ScheduleDB.commit()
        
        return fetch(fno) if dep_time == "" else update(fno, dep_time)

    @staticmethod
    def add_flight(fno: str, dep_time: str) -> None:
        Schedule.cursor.execute("SELECT flight_no FROM Schedule")
        fnos = [i[0] for i in Schedule.cursor.fetchall()]
        
        if fno in fnos:
            return
        
        Schedule.cursor.execute(f'INSERT INTO Schedule VALUES ("{fno}","{dep_time}")')
        Schedule.ScheduleDB.commit()

    @staticmethod
    def remove_flight(fno: str) -> None:
        Schedule.cursor.execute(f'DELETE FROM Schedule WHERE flight_no="{fno}" ')
        Schedule.ScheduleDB.commit()
        
    @staticmethod
    def check_schedule(fno: str) -> bool:
        curr_time = datetime.now()
        dep_time = datetime.fromisoformat(str(Schedule.dep_time(fno)))
        
        if curr_time > dep_time:
            Schedule.remove_flight(fno)
            return True
        else:
            return False