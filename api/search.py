from requests import Response
from .client import ApiClient


class SearchApi:
    def __init__(self, client: ApiClient) -> None:
        self.client = client

    def search(
            self,
            query: str,
            offset: int | None = None,
            limit: int | None = None,
            is_highlight: bool | None = None,
            title: bool | None = None,
            tags: bool | None = None,
            department_id: int | None = None,
            has_images: bool | None = None,
            date_begin: int | None = None,
            date_end: int | None = None,
    ) -> Response:
        params = {
            "q": query,
            "offset": offset,
            "limit": limit,
            "isHighlight": is_highlight,
            "title": title,
            "tags": tags,
            "departmentId": department_id,
            "hasImages": has_images,
            "dateBegin": date_begin,
            "dateEnd": date_end,
        }

        params = {
            key: value
            for key, value in params.items()
            if value is not None
        }

        return self.client.get(
            endpoint="search",
            version="v1.1",
            params=params,
        )

    # Поиск с явно заданным порядком query-параметров.
    def search_raw(self, params: list[tuple[str, str]]) -> Response:

        return self.client.get(
            endpoint="search",
            version="v1.1",
            params=params,
        )
