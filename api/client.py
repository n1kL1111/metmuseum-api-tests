import requests


class ApiClient:
    BASE_URL = "https://collectionapi.metmuseum.org/public/collection"

    def __init__(self, session: requests.Session):
        self.session = session

    def get(
        self,
        endpoint: str,
        *,
        version: str = "v1",
        params: dict | None = None,
    ):
        response = self.session.get(
            f"{self.BASE_URL}/{version}/{endpoint}",
            params=params,
        )

        response.raise_for_status()

        return response
