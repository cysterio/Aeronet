import mysql.connector as db
from Utils.Credentials.CredUtils import Credentials

class Aeronet:
    def get_valid_connection(self) -> object:
        password = Credentials.get_password()
        if not password:
            password = input("Please enter your mysql password : ")

        while True:
            try:
                myDB = db.connect(
                    host="localhost", 
                    user="root", 
                    password=password
                )
                Credentials.set_password(password)
                return myDB
            except db.errors.ProgrammingError:
                if not password == "Aeronet@123":
                    print("Wrong Password, Try Again")
                password = input("Please enter your mysql password : ")

    def initialize_database(self, cursor : object) -> None:
        cursor.execute("CREATE DATABASE IF NOT EXISTS Aeronet")
        cursor.execute("USE Aeronet")

        tables = {
            "FlightPath": """
                CREATE TABLE IF NOT EXISTS FlightPath (
                    flight_no VARCHAR(8),
                    waypoint VARCHAR(200),
                    dist_from_wp DECIMAL(4, 2),
                    rate_assign VARCHAR(7)
                )
            """,
            "FM_Data": """
                CREATE TABLE IF NOT EXISTS FM_Data (
                    flight_no VARCHAR(15),
                    heading INT,
                    coordinates VARCHAR(90),
                    altitude INT,
                    air_speed INT,
                    climb_rate INT
                )
            """,
            "Schedule": """
                CREATE TABLE IF NOT EXISTS Schedule (
                    flight_no VARCHAR(8),
                    dep_time VARCHAR(25)
                )
            """,
            "Weather": """
                CREATE TABLE IF NOT EXISTS Weather (
                    description VARCHAR(18),
                    precipitation INT,
                    wind_speed INT,
                    cloud_base INT,
                    last_updated VARCHAR(25)
                )
            """
        }

        for query in tables.values():
            cursor.execute(query)

        for table in tables.keys():
            cursor.execute(f"DELETE FROM {table}")

        cursor.execute("""
            INSERT INTO Weather VALUE(
                "Sunny",
                10,
                0,
                6500,
                "2024-08-01 19:09:00"
            )
        """)

    def main(self) -> None:
        myDB = self.get_valid_connection()
        cursor = myDB.cursor()
        
        self.initialize_database(cursor)
        
        myDB.commit()
        
        from Interface.Interface import Interface
        Interface()

if __name__ == "__main__":
    Aeronet = Aeronet()
    Aeronet.main()
