import allure
from requests import Response

from .client import ApiClient


class DepartmentsApi:
    def __init__(self, client: ApiClient):
        self.client = client

    @allure.step("Получить список отделов музея")
    def get_departments(self) -> Response:
        return self.client.get("departments")
