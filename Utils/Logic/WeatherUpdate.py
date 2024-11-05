import numpy as np
from datetime import datetime
from Utils.Update.WeatherUtils import Weather

class WeatherUpdate:
    @staticmethod
    def auto_update() -> None:
        if WeatherUpdate.check_time():
            desc, preci, speed, base = WeatherUpdate.get_weather()
            
            Weather.description(desc)
            Weather.precipitation(preci)
            Weather.wind_speed(speed)
            Weather.cloud_base(base)
            Weather.last_updated(str(datetime.now())[0:19])

    @staticmethod
    def check_time() -> bool:
        current_datetime = datetime.now()
        last_update = datetime.fromisoformat(Weather.last_updated())
        delta = abs(current_datetime - last_update).total_seconds()
        return delta > 7200

    @staticmethod
    def get_weather() -> tuple[str, int, int, int]:
        events = ["Sunny", "Cloudy", "Thunderstorms", "Fog"]
        probables = [0.50, 0.30, 0.08, 0.12]
        desc = np.random.choice(events, size=1, p=probables)[0]
        
        match desc:
            case "Sunny":
                preci = np.random.randint(0, 30)
                speed = np.random.randint(5, 35)
                base = np.random.randint(4500, 8000)
            case "Cloudy":
                preci = np.random.randint(20, 60)
                speed = np.random.randint(10, 40)
                base = np.random.randint(3000, 5000)
            case "Thunderstorms":
                preci = np.random.randint(70, 100)
                speed = np.random.randint(30, 60)
                base = np.random.randint(3000, 5000)
            case "Fog":
                preci = np.random.randint(65, 90)
                speed = np.random.randint(5, 20)
                base = np.random.randint(2000, 3500)
        
        return desc, preci, speed, base
