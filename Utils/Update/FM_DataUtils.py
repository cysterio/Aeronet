import mysql.connector as db
from Utils.Credentials.CredUtils import Credentials

class FM_Data:
    FM_DataDB = db.connect(
        user="root",
        password=Credentials.get_password(),
        host="localhost",
        database="Aeronet"
    )

    cursor = FM_DataDB.cursor()

    @staticmethod
    def heading(fno: str, hdg: int = -1) -> int:
        def fetch(fno: str) -> int:
            FM_Data.cursor.execute(
                f"""
                SELECT heading 
                FROM FM_Data 
                WHERE flight_no = "{fno}"
                """
            )
            return FM_Data.cursor.fetchone()[0]

        def update(fno: str, hdg: int) -> None:
            FM_Data.cursor.execute(
                f"""
                UPDATE FM_Data 
                SET heading = {hdg} 
                WHERE flight_no = "{fno}"
                """
            )
            FM_Data.FM_DataDB.commit()
        
        return fetch(fno) if hdg == -1 else update(fno, hdg)

    @staticmethod
    def coordinates(fno: str, ord: str = "") -> tuple:
        def fetch(fno: str) -> tuple:
            FM_Data.cursor.execute(
                f"""
                SELECT coordinates 
                FROM FM_Data 
                WHERE flight_no = "{fno}"
                """
            )
            ords = FM_Data.cursor.fetchone()[0][1:-1].split(",")
            return tuple(eval(f"({float(ords[0])}, {float(ords[1])})"))

        def update(fno: str, ord: str) -> None:
            FM_Data.cursor.execute(
                f"""
                UPDATE FM_Data 
                SET coordinates = "{ord}" 
                WHERE flight_no = "{fno}"
                """
            )
            FM_Data.FM_DataDB.commit()
        
        return fetch(fno) if ord == "" else update(fno, ord)

    @staticmethod
    def altitude(fno: str, alt: float = -1) -> float:
        def fetch(fno: str) -> float:
            FM_Data.cursor.execute(
                f"""
                SELECT altitude 
                FROM FM_Data 
                WHERE flight_no = "{fno}"
                """
            )
            return FM_Data.cursor.fetchone()[0]

        def update(fno: str, alt: float) -> None:
            FM_Data.cursor.execute(
                f"""
                UPDATE FM_Data 
                SET altitude = {alt} 
                WHERE flight_no = "{fno}"
                """
            )
            FM_Data.FM_DataDB.commit()
        
        return fetch(fno) if alt == -1 else update(fno, alt)

    @staticmethod
    def air_speed(fno: str, speed: float = -1) -> float:
        def fetch(fno: str) -> float:
            FM_Data.cursor.execute(
                f"""
                SELECT air_speed 
                FROM FM_Data 
                WHERE flight_no = "{fno}"
                """
            )
            return FM_Data.cursor.fetchone()[0]

        def update(fno: str, speed: float) -> None:
            FM_Data.cursor.execute(
                f"""
                UPDATE FM_Data 
                SET air_speed = {speed} 
                WHERE flight_no = "{fno}"
                """
            )
            FM_Data.FM_DataDB.commit()
        
        return fetch(fno) if speed == -1 else update(fno, speed)

    @staticmethod
    def climb_rate(fno: str, rate: float = -1) -> float:
        def fetch(fno: str) -> float:
            FM_Data.cursor.execute(
                f"""
                SELECT climb_rate 
                FROM FM_Data 
                WHERE flight_no = "{fno}"
                """
            )
            return FM_Data.cursor.fetchone()[0]

        def update(fno: str, rate: float) -> None:
            FM_Data.cursor.execute(
                f"""
                UPDATE FM_Data 
                SET climb_rate = {rate} 
                WHERE flight_no = "{fno}"
                """
            )
            FM_Data.FM_DataDB.commit()
        
        return fetch(fno) if rate == -1 else update(fno, rate)

    @staticmethod
    def add_flight_data(fno: str, hdg: int, ord: str, alt: float, sped: float, rate: float) -> None:
        FM_Data.cursor.execute(
            f"""
            INSERT INTO FM_Data 
            VALUES ("{fno}", {hdg}, "{ord}", {alt}, {sped}, {rate})
            """
        )
        FM_Data.FM_DataDB.commit()

    @staticmethod
    def remove_flight_data(fno: str) -> None:
        FM_Data.cursor.execute(
            f"""
            DELETE FROM FM_Data 
            WHERE flight_no = "{fno}"
            """
        )
        FM_Data.FM_DataDB.commit()

    @staticmethod
    def get_current_coords() -> list:
        FM_Data.cursor.execute(
            """
            SELECT flight_no, coordinates 
            FROM FM_Data
            """
        )
        return [(i, eval(j)) for i, j in FM_Data.cursor.fetchall()]

    @staticmethod
    def get_proxy_altitudes(fno: list) -> list:
        FM_Data.cursor.execute(
            f"""
            SELECT altitude 
            FROM FM_Data 
            WHERE flight_no IN {tuple(fno) + ('', '')}
            """
        )
        return [(i[0]) for i in FM_Data.cursor.fetchall()]

    @staticmethod
    def get_all_fno() -> list:
        FM_Data.cursor.execute(
            """
            SELECT flight_no 
            FROM FM_Data
            """
        )
        return [i[0] for i in FM_Data.cursor.fetchall()]
