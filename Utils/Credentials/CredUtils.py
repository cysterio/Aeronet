import os
import json

class Credentials:
    path: str = os.path.join(os.path.dirname(__file__), "Credentials.json")
    
    @staticmethod
    def get_password() -> str:
        with open(Credentials.path, "r") as file:
            return json.load(file)["password"]

    @staticmethod
    def set_password(password: str) -> None:
        with open(Credentials.path, "w") as file:
            json.dump({"password": password}, file)
