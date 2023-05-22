import requests


class API_interface(object):
    def __init__(self, url: str, token: str):
        self._headers = {
            "Authorization": f"Bearer {token}",
            "content-type": "application/json",
        }
        self._url = url

    def __str__(self) -> str:
        return f"{self._url}/lovelace/default_view"

    def post(self, endpoint: str, data: object) -> str:
        response = requests.post(
            url=f"{self._url}{endpoint}", headers=self._headers, json=data
        )
        return response.text

    def get(self, endpoint: str) -> str:
        response = requests.get(url=f"{self._url}{endpoint}", headers=self._headers)
        return response.text
