from requests import Response

from .client import ApiClient


class ObjectsApi:
    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def get_object(self, object_id: int) -> Response:
        return self.client.get(f"objects/{object_id}")

    def get_objects(
        self,
        department_ids: str | None = None,
        metadata_date: str | None = None,
    ) -> Response:
        params = {
            "departmentIds": department_ids,
            "metadataDate": metadata_date,
        }
        params = {
            key: value
            for key, value in params.items()
            if value is not None
        }

        return self.client.get("objects", params=params)
