# utils/api_client.py
import requests


class StellarApi:
    BASE_URL = "https://stellarburgers.education-services.ru"

    def register_user(self, email: str, password: str, name: str):
        return requests.post(
            f"{self.BASE_URL}/api/auth/register",
            json={"email": email, "password": password, "name": name},
            timeout=30,
        )

    def login_user(self, email: str, password: str):
        return requests.post(
            f"{self.BASE_URL}/api/auth/login",
            json={"email": email, "password": password},
            timeout=30,
        )

    def delete_user(self, access_token: str):
        return requests.delete(
            f"{self.BASE_URL}/api/auth/user",
            headers={"Authorization": access_token},
            timeout=30,
        )
