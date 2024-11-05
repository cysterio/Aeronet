import mysql.connector as db
from Utils.Credentials.CredUtils import Credentials

class FlightPath:
    FlightPathDB = db.connect(
        user="root",
        password=Credentials.get_password(),
        host="localhost",
        database="Aeronet"
    )

    cursor = FlightPathDB.cursor()

    @staticmethod
    def waypoints(fno: str, wayp: str = None) -> str:
        def fetch(fno: str) -> str:
            FlightPath.cursor.execute(
                f"""
                SELECT waypoint 
                FROM FlightPath 
                WHERE flight_no = "{fno}"
                """
            )
            return FlightPath.cursor.fetchone()[0]

        def update(fno: str, wayp: str) -> None:
            FlightPath.cursor.execute(
                f"""
                UPDATE FlightPath 
                SET waypoint = "{wayp}" 
                WHERE flight_no = "{fno}"
                """
            )
            FlightPath.FlightPathDB.commit()

        return fetch(fno) if wayp is None else update(fno, wayp)

    @staticmethod
    def dist_from_waypoint(fno: str, dist: float = None) -> float:
        def fetch(fno: str) -> float:
            FlightPath.cursor.execute(
                f"""
                SELECT dist_from_wp 
                FROM FlightPath 
                WHERE flight_no = "{fno}"
                """
            )
            return float(FlightPath.cursor.fetchone()[0])

        def update(fno: str, dist: float) -> None:
            FlightPath.cursor.execute(
                f"""
                UPDATE FlightPath 
                SET dist_from_wp = {dist} 
                WHERE flight_no = "{fno}"
                """
            )
            FlightPath.FlightPathDB.commit()

        return fetch(fno) if dist is None else update(fno, dist)

    @staticmethod
    def rate_assign(fno: str, rate: str = None) -> str:
        def fetch(fno: str) -> str:
            FlightPath.cursor.execute(
                f"""
                SELECT rate_assign 
                FROM FlightPath 
                WHERE flight_no = "{fno}"
                """
            )
            return FlightPath.cursor.fetchone()[0]

        def update(fno: str, rate: str) -> None:
            FlightPath.cursor.execute(
                f"""
                UPDATE FlightPath 
                SET rate_assign = "{rate}" 
                WHERE flight_no = "{fno}"
                """
            )
            FlightPath.FlightPathDB.commit()

        return fetch(fno) if rate is None else update(fno, rate)

    @staticmethod
    def add_flight_path(fno: str, waypoints: str, dist_from_wp: float, rate_assign: str) -> None:
        FlightPath.cursor.execute(
            f"""
            INSERT INTO FlightPath 
            VALUES ("{fno}", "{waypoints}", {dist_from_wp}, "{rate_assign}")
            """
        )
        FlightPath.FlightPathDB.commit()

    @staticmethod
    def remove_flight_path(fno: str) -> None:
        FlightPath.cursor.execute(
            f"""
            DELETE FROM FlightPath 
            WHERE flight_no = "{fno}"
            """
        )
        FlightPath.FlightPathDB.commit()

    @staticmethod
    def count_traffic() -> int:
        FlightPath.cursor.execute(
            """
            SELECT count(*) 
            FROM FlightPath
            """
        )
        return FlightPath.cursor.fetchone()[0]