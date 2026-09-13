from requests import Response

from .client import ApiClient


class DepartmentsApi:
    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def get_departments(self) -> Response:
        return self.client.get("departments")
