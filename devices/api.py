import requests
import urllib.parse
import re
import exceptions.exceptions as exceptions


class API_interface(object):
    def __init__(self, url: str, token: str):
        self._headers = {
            "Authorization": f"Bearer {token}",
            "content-type": "application/json",
        }
        self._url = url
        if not re.compile("https?://.*").fullmatch(self._url):
            self._url = f"http://{self._url}"

        if self._url[-1] == "/":
            self._url = self._url[:-1]

        parsed_url = urllib.parse.urlsplit(self._url)
        if (
            parsed_url.query
            or parsed_url.fragment
            or parsed_url.path
            or not parsed_url.netloc
        ):
            raise exceptions.InvalidURL(self._url)

        try:
            self.get(endpoint="/api/")
        except:
            raise exceptions.HassioUnreachable(self._url)

    def __str__(self) -> str:
        return f"{self._url}/lovelace/default_view"

    def __getitem__(self, key) -> str:
        if key == "url":
            return self._url
        else:
            raise KeyError

    def post(self, endpoint: str, data: object) -> str:
        response = requests.post(
            url=f"{self._url}{endpoint}", headers=self._headers, json=data
        )
        return response.text

    def get(self, endpoint: str) -> str:
        response = requests.get(url=f"{self._url}{endpoint}", headers=self._headers)
        return response.text
