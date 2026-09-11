from requests import Response

from .client import ApiClient


class DepartmentsApi:
    def __init__(self, client: ApiClient):
        self.client = client

    def get_departments(self) -> Response:
        return self.client.get("departments")

    def get_department(self, department_id: int) -> Response:
        return self.client.get(f"departments/{department_id}")
