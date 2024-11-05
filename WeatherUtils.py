import mysql.connector as db
from Utils.Credentials.CredUtils import Credentials

class Weather:
    WeatherDB = db.connect(user="root", 
                           host="localhost",
                           password=Credentials.get_password(), 
                           database="Aeronet")
    
    cursor = WeatherDB.cursor()
    
    @staticmethod
    def description(desc: str = "") -> str:
        def fetch() -> str:
            Weather.cursor.execute("SELECT description FROM Weather")
            return Weather.cursor.fetchone()[0]
            
        def update(desc: str) -> None:
            Weather.cursor.execute(f'UPDATE Weather SET description = "{desc}"')
            Weather.WeatherDB.commit()
        
        return fetch() if desc == "" else update(desc)
        
    @staticmethod
    def precipitation(ppt: float = -1) -> float:
        def fetch() -> float:
            Weather.cursor.execute("SELECT precipitation FROM Weather")
            return Weather.cursor.fetchone()[0]

        def update(ppt: float) -> None:
            Weather.cursor.execute(f'UPDATE Weather SET precipitation = {ppt}')
            Weather.WeatherDB.commit()
        
        return fetch() if ppt == -1 else update(ppt)

    @staticmethod
    def wind_speed(ws: float = -1) -> float:
        def fetch() -> float:
            Weather.cursor.execute("SELECT wind_speed FROM Weather")
            return Weather.cursor.fetchone()[0]

        def update(ws: float) -> None:
             Weather.cursor.execute(f'UPDATE Weather SET wind_speed = {ws}')
             Weather.WeatherDB.commit()
        
        return fetch() if ws == -1 else update(ws)
    
    @staticmethod
    def cloud_base(cb: int = 0) -> int:
        def fetch() -> int:
            Weather.cursor.execute("SELECT cloud_base FROM Weather")
            return Weather.cursor.fetchone()[0]

        def update(cb: int) -> None:
             Weather.cursor.execute(f'UPDATE Weather SET cloud_base = {cb}')
             Weather.WeatherDB.commit()
        
        return fetch() if cb == 0 else update(cb)

    @staticmethod
    def last_updated(lu: str = "") -> str:
        def fetch() -> str:
            Weather.cursor.execute("SELECT last_updated FROM Weather")
            return Weather.cursor.fetchone()[0]

        def update(lu: str) -> None: 
            Weather.cursor.execute(f'UPDATE Weather SET last_updated = "{lu}"')
            Weather.WeatherDB.commit()

        return fetch() if lu == "" else update(lu)