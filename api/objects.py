import allure
from requests import Response

from .client import ApiClient


class ObjectsApi:
    def __init__(self, client: ApiClient):
        self.client = client

    @allure.step("Получить произведение искусства по ID: {object_id}")
    def get_object(self, object_id: int) -> Response:
        return self.client.get(f"objects/{object_id}")

    @allure.step("Получить список произведений искусства")
    def get_objects(self) -> Response:
        return self.client.get("objects")